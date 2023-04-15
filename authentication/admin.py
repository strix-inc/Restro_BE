from django.contrib import admin
from authentication.models import Member, Restaurant

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "contact")
