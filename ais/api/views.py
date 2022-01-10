from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from celery.decorators import task
from django.core import serializers

import requests
import time

from .models import Token
from .models import Access
from .models import Account
from .models import Transaction


def home(request):
    return JsonResponse({'home': 'hello!'})


def connect_account(request):
    """
     Renders the bank_selector by Nordigen https://github.com/nordigen/nordigen-bank-ui
     Returns: html with the UI
    """
    banks = institutions_list(request, 'ES')
    return render(request, "index.html", {'banks': banks})


def institutions_list(request, country='LV'):
    """
     Request to institutions endpoint to get all the institutions given a country code. Is used for the bank selector UI
     Returns: list of institutions
    """
    headers = {
        'accept': 'application/json',
        'Authorization': get_token_header(request)
    }
    url = f'https://ob.nordigen.com/api/v2/institutions/?country={country}'
    response = requests.get(url, headers=headers)
    return response.text


def process_connection(request, bank_id):
    """
     Starts a bank connection process given a bank_id selected from the bank selector UI, will return the necessary
     resources to finish the connection.
     Returns: requisition_id, link
    """
    agreement_id = end_user_agreement(request, bank_id)
    requisition = requisitions(request, bank_id, agreement_id)
    return JsonResponse({
        'status': 'succeed',
        'requisition_id': requisition['id'],
        'link': requisition['link']
    })


def end_user_agreement(request, bank_id):
    """
     Request to retrieve the agreement id and proceed with the connection
     Returns: agreement_id
    """
    headers = {
        'Authorization': get_token_header(request)
    }
    data = {
        'institution_id': bank_id,
        'max_historical_days': '180',
        'access_valid_for_days': '30',
        'access_scope': [
            'balances',
            'details',
            'transactions'
        ]
    }
    url = 'https://ob.nordigen.com/api/v2/agreements/enduser/'
    response = requests.post(url, json=data, headers=headers)
    return response.json()['id']


def requisitions(request, bank_id, agreement_id):
    """
     Gets the requisition needed to finish the bank account connection
     Returns: requisition_id, requisition_link
    """
    data = {
        'institution_id': bank_id,
        'reference': generate_reference(),
        'redirect': 'https://ob.nordigen.com/',
        'agreement': agreement_id,
        'user_language': 'EN'
    }
    headers = {
        'Authorization': get_token_header(request)
    }
    url = 'https://ob.nordigen.com/api/v2/requisitions/'
    response = requests.post(url, json=data, headers=headers)
    return response.json()


def list_accounts(request, requisition_id):
    """
     List accounts for a given requisition_id. Will also persist those accounts into the BD.
     Returns: list of accounts
    """
    url = f'https://ob.nordigen.com/api/v2/requisitions/{requisition_id}/'
    headers = {
        'accept': 'application/json',
        'Authorization': get_token_header(request)
    }
    response = requests.get(url, headers=headers)

    for account in response.json()['accounts']:
        updated_values = {
            'account_id': account,
        }
        Account.objects.update_or_create(
            user=request.user,
            account_id=account,
            defaults=updated_values
        )

    return HttpResponse(
        content=JsonResponse({'accounts': response.json()['accounts']}),
        status=response.status_code,
        content_type=response.headers['Content-Type']
    )


def create_access(request):
    """
     Generates access needed to use the Nordigen API
     Returns: access, refresh
    """
    queryset = Token.objects.all().filter(user=request.user).first()
    url = 'https://ob.nordigen.com/api/v2/token/new/'
    data = {
        'secret_id': queryset.secret_id,
        'secret_key': queryset.secret_key
    }
    response = requests.post(url, json=data)

    updated_values = {
        'access': response.json()['access'],
        'refresh': response.json()['refresh']
    }
    Access.objects.update_or_create(
        user=request.user,
        defaults=updated_values
    )
    return HttpResponse(
        content=response.content,
        status=response.status_code,
        content_type=response.headers['Content-Type']
    )


def refresh_access(request):
    """
     Refreshes the access token needed for the Nordigen API
     Returns: access
    """
    queryset = Access.objects.all().filter(user=request.user).first()
    url = 'https://ob.nordigen.com/api/v2/token/refresh/'
    data = {
        'refresh': queryset.refresh
    }
    response = requests.post(url, json=data)

    updated_values = {
        'access': response.json()['access']
    }
    Access.objects.update_or_create(
        user=request.user,
        defaults=updated_values
    )
    return HttpResponse(
        content=response.content,
        status=response.status_code,
        content_type=response.headers['Content-Type']
    )


def details(request, account_id):
    """
     Gets the account details for a given account_id
     Returns: account
    """
    url = f'https://ob.nordigen.com/api/v2/accounts/premium/{account_id}/details/'
    headers = {
        'accept': 'application/json',
        'Authorization': get_token_header(request)
    }
    response = requests.get(url, headers=headers)
    return HttpResponse(
        content=response.content,
        status=response.status_code,
        content_type=response.headers['Content-Type']
    )


def balances(request, account_id):
    """
     Gets the balances for a given account_id
     Returns: balances
    """
    url = f'https://ob.nordigen.com/api/v2/accounts/{account_id}/balances/'
    headers = {
        'accept': 'application/json',
        'Authorization': get_token_header(request)
    }
    response = requests.get(url, headers=headers)
    return HttpResponse(
        content=response.content,
        status=response.status_code,
        content_type=response.headers['Content-Type']
    )


def transactions(request, account_id):
    """
     Gets the transactions for a given account_id
    """
    qs = Transaction.objects.all().filter(account=account_id)
    serialized_qs = serializers.serialize('json', qs, )
    return JsonResponse({'transactions': serialized_qs})


def get_transactions(request, account_id):
    """
     Computes the transactions for a given account_id asynchronously. The list endpoint will be used to query this list
    """
    token = get_token_header(request)
    request_transaction.delay(token, account_id)
    return JsonResponse({'status': 1})


@task(name="transactions")
def request_transaction(token, account_id):
    """
     Celery task to compute transactions for a given account
    """
    url = f'https://ob.nordigen.com/api/v2/accounts/premium/{account_id}/transactions/?date_from=2021-12-30&date_to=2022-01-10'
    headers = {
        'accept': 'application/json',
        'Authorization': token
    }
    response = requests.get(url, headers=headers)
    transactions = response.json()['transactions']
    booked = transactions['booked']
    account = Account.objects.all().filter(account_id=account_id).first()

    for transaction in booked:
        amount = transaction['transactionAmount']
        category = transaction['categorisation']
        updated_values = {
            'account': account,
            'amount': amount['amount'],
            'currency': amount['currency'],
            'details': transaction['remittanceInformationUnstructured'],
            'category_id': category['categoryId'],
            'category_title': category['categoryTitle'],
            'date': transaction['bookingDate']
        }
        Transaction.objects.update_or_create(
            account=account,
            details=transaction['remittanceInformationUnstructured'],
            date=transaction['bookingDate'],
            amount=amount['amount'],
            defaults=updated_values
        )


def generate_reference():
    """
     Generates unique reference for the account setup
     Returns: reference
    """
    return int(str(time.time()).replace('.', ''))


def get_token_header(request):
    """
     Gets the token header for a registered user.
     Returns: token
    """
    return f'Bearer {Access.objects.all().filter(user=request.user).first().access}'
