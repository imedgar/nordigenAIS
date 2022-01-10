from django.contrib import admin
from .models import Token
from .models import Access
from .models import Account
from .models import Transaction

# Register your models here.

admin.site.register(Token)
admin.site.register(Access)
admin.site.register(Account)
admin.site.register(Transaction)