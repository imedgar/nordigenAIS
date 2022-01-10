from django.db import models
from django.conf import settings

# Create your models here.


class Token(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    secret_id = models.CharField(max_length=50)
    secret_key = models.CharField(max_length=250)

    def __str__(self):
        return self.secret_id


class Access(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    access = models.CharField(max_length=250)
    refresh = models.CharField(max_length=250)

    def __str__(self):
        return self.access + '.' + self.refresh


class Account(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    account_id = models.CharField(max_length=50)

    def __str__(self):
        return self.account_id


class Transaction(models.Model):
    account = models.CharField(max_length=50)
    amount = models.CharField(max_length=100)
    currency = models.CharField(max_length=10)
    category_id = models.CharField(max_length=10, default='')
    category_title = models.CharField(max_length=50)
    details = models.CharField(max_length=250)
    date = models.CharField(max_length=20, default='')
