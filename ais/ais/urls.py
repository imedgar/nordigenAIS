"""ais URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import connect_account
from api.views import process_connection
from api.views import home
from api.views import list_accounts
from api.views import create_access
from api.views import refresh_access
from api.views import details
from api.views import balances
from api.views import get_transactions
from api.views import transactions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('access/create', create_access),
    path('access/refresh', refresh_access),
    path('account/select', connect_account),
    path('account/<slug:bank_id>/connect', process_connection),
    path('account/<slug:requisition_id>/list', list_accounts),
    path('account/<slug:account_id>/details', details),
    path('account/<slug:account_id>/balances', balances),
    path('account/<slug:account_id>/transactions', get_transactions),
    path('account/<slug:account_id>/transactions/list', transactions),
    path('', home),
]
