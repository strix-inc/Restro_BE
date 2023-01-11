from django.db import models

from kitchen.models.food import Dish
from kitchen.models.platform import Platform
from .base import BaseFinanceModel


class Bill(BaseFinanceModel):
    # * Money
    subtotal = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)
    cgst = models.FloatField(default=0.0)
    sgst = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)

    # * Meta
    finalized = models.BooleanField(default=False)
    table = models.CharField(max_length=32)
    platform = models.ForeignKey(Platform, on_delete=models.DO_NOTHING, null=True, blank=True)


class KOT(BaseFinanceModel):
    bill = models.ForeignKey(Bill, on_delete=models.DO_NOTHING)


class Order(BaseFinanceModel):
    class Size(models.TextChoices):
        HALF = "half"
        FULL = "full"

    dish = models.ForeignKey(Dish, on_delete=models.DO_NOTHING)
    kot = models.ForeignKey(KOT, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    size = models.CharField(max_length=16, choices=Size.choices, default=Size.FULL)
