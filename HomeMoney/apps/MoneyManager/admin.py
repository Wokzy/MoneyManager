from django.contrib import admin
from .models import Account, Change, Category

admin.site.register(Account)
admin.site.register(Change)
admin.site.register(Category)