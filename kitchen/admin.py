from django.contrib import admin
from .models import Dish, DishRate, Category, Platform

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "restaurant")


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    search_fields = ("name", "restaurant__name")
    list_display = ("name", "category", "restaurant")

@admin.register(DishRate)
class DishRateAdmin(admin.ModelAdmin):
    search_fields = ("dish__name", "restaurant__name")
    list_display = ("dish", "restaurant", "platform", "half_price", "full_price")
