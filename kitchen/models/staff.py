from django.db import models
from .base import BaseKitchenModel


class Staff(BaseKitchenModel):
    name = models.CharField(max_length=64)
    contact = models.CharField(max_length=16, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("name", "restaurant")
