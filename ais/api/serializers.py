from rest_framework import serializers
from .models import Token
from .models import Access
from .models import Account
from .models import Transaction


class TokenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Token
        fields = ('user', 'secret_id', 'secret_key')


class AccessSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Access
        fields = ('user', 'access', 'refresh')


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Account:
        model = Account
        fields = ('user', 'account_id')


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Transaction:
        model = Transaction
        fields = ('account', 'amount', 'currency', 'details', 'category_id', 'category_title', 'date')
