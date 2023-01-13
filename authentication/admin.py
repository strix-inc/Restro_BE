from django.contrib import admin
from authentication.models import Member, Restaurant

# Register your models here.
admin.site.register([Member, Restaurant])
