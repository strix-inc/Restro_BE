from django.db import models
from authentication.models.restaurant import Restaurant
from restrofin.base_model import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=64)
    restaurant = models.ForeignKey(Restaurant)
