from django.db import models

from authentication.models.restaurant import Restaurant
from restrofin.base_model import BaseModel


class BaseKitchenModel(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    class Meta:
        abstract = True
