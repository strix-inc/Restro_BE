from django.db import models

from kitchen.models.food import Dish
from kitchen.models.platform import Platform
from kitchen.models.staff import Staff
from .base import BaseFinanceModel


class Customer(BaseFinanceModel):
    contact = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=64, null=True, blank=True)


class Invoice(BaseFinanceModel):
    class PaymentType(models.TextChoices):
        CASH = "Cash"
        UPI = "UPI"
        CARD = "Card"

    class PaymentStatus(models.TextChoices):
        PENDING = "Pending"
        PAID = "Paid"

    # * Money
    subtotal = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)
    cgst = models.FloatField(default=0.0)
    sgst = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)
    payment_type = models.CharField(
        max_length=32, choices=PaymentType.choices, default=PaymentType.CASH
    )

    # * Meta
    finalized = models.BooleanField(default=False)
    table = models.CharField(max_length=32)
    platform = models.ForeignKey(
        Platform, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    invoice_number = models.PositiveBigIntegerField(default=1)
    amount_paid = models.FloatField(default=0.0)
    customer = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    staff = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, null=True, blank=True)

    @property
    def amount_due(self):
        return self.total - self.amount_paid

    @property
    def payment_status(self):
        return self.PaymentStatus.PENDING if self.amount_due > 0 else self.PaymentStatus.PENDING

    def calculate_total(self):
        return (self.subtotal - self.discount) + self.cgst + self.sgst

    def save(self, *args, **kwargs):
        if not self.pk:
            last_count = self.objects.all(restaurant=self.restaurant).count()
            self.invoice_number = last_count + 1

        self.total = round(self.calculate_total(), 2)
        self.subtotal = round(self.subtotal, 2)
        self.cgst = round(self.cgst, 2)
        self.sgst = round(self.sgst, 2)
        super().save(*args, **kwargs)


class KOT(BaseFinanceModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.DO_NOTHING)
    items = models.JSONField(default=list) # * [{"id": "123", "name": "Chicken", "quantity": 1, "size": "Half"}]


class Order(BaseFinanceModel):
    class Size(models.TextChoices):
        HALF = "Half"
        FULL = "Full"

    dish = models.ForeignKey(Dish, on_delete=models.DO_NOTHING)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    size = models.CharField(max_length=16, choices=Size.choices, default=Size.FULL)
    cost = models.FloatField(default=0.0)
