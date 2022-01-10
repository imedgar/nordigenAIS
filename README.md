# nordigen AIS

AIS is a service to consume nordigen AIS API

## Dependencies

- Django (https://www.djangoproject.com/)
- DRF djangorestframework (https://www.django-rest-framework.org/)
- Celery (https://docs.celeryproject.org/en/stable/)
- Redis (https://redis.io/)
- nordigen-bank-ui (https://github.com/nordigen/nordigen-bank-ui)

```bash
pip3 install requirements.txt
```

## Installation

Create a virtual environment
```bash
python3 -m venv nordigen
```

Activate the venv
```bash
source nordigen/bin/activate
```

Install the dependencies
```bash
pip3 install -r requirements.txt
```

Install the nordigen-bank-ui
```bash
npm install
```

## Start

Create a virtual environment
```bash
python3 
```

Start the redis server in a different terminal
```bash
redis-server
```

Start the celerys worker
```bash
celery -A ais worker -l info
```

Run the migrations
```bash
python3 manage.py makemigrations
```
```bash
python3 manage.py migrate
```

Start the server, be sure to be located where manage.py is (ais)
```bash
python3 manage.py runserver
```

## AIS usage

create a superuser
```bash
python3 manage.py createsuperuser
```

Set a secret key in nordigen to use against its API (https://ob.nordigen.com/user-secrets/)

Once the secret key it's created we will use it to create access token
```bash
python3 manage.py createsuperuser
```

Request from the browser or if you log in Django with 
```
http://localhost:8000/access/create
```

Connect and account from
```
http://localhost:8000/account/select
```

The response should be 
```json
{"status": "succeed", "requisition_id": "requisition_id", "link": "https://ob.nordigen.com/psd2/start/requisition_id/bank_id"}
```

Use the link to connect your bank account and the requisition_id to list the accounts once is set
```
http://localhost:8000/account/<requisition_id>/list
```

The response will be a list of accounts for the given requisition_id.
To get account data use its id as
```
http://localhost:8000/account/<account_id>/details
```
```
http://localhost:8000/account/<account_id>/balances
```

For the transaction we will have to compute them before accessing the data
```
http://localhost:8000/account/<account_id>/transactions
```
After a while the data can be accesses like this
```
http://localhost:8000/account/<account_id>/transactions/list
```

## Author
Edgar (https://github.com/imedgar)