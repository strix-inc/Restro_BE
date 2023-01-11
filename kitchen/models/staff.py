from django.db import models
from restrofin.base_model import BaseModel
from authentication.models.restaurant import Restaurant


class Staff(BaseModel):
    name = models.CharField()
    contact = models.BigIntegerField()
    address = models.CharField()
    date_of_joining = models.DateField()
    restaurant = models.ForeignKey(Restaurant)
