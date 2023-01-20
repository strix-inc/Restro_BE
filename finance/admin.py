from django.contrib import admin
from finance.models.sale import Customer, Invoice, KOT, Order

# Register your models here.
admin.site.register([Customer, Invoice, KOT, Order])