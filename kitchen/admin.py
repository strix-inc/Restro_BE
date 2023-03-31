from django.contrib import admin
from .models import Dish, DishRate, Category, Platform

admin.site.register([DishRate, Dish, Category, Platform])
