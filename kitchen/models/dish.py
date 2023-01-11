from django.db import models
from restrofin.base_model import BaseModel
from authentication.models.restaurant import Restaurant


class Dish():
    name = models.CharField(max_length=32)
    restro_half_price = models.IntegerField(null=True, blank=True)
    restro_full_price = models.IntegerField()
    zomato_half_price = models.IntegerField()
    zomato_full_price = models.IntegerField()
    swiggy_half_price = models.IntegerField()
    swiggy_full_price = models.IntegerField()
    restaurant = models.ForeignKey(Restaurant)



