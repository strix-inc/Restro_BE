from django.db import models

from kitchen.models.food import Dish
from kitchen.models.platform import Platform
from kitchen.models.staff import Staff
from .base import BaseFinanceModel


class Customer(BaseFinanceModel):
    contact = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=64, null=True, blank=True)


class Invoice(BaseFinanceModel):
    CGST_PERCENT = 0.025
    SGST_PERCENT = 0.025

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
    invoice_number = models.PositiveBigIntegerField(null=True, blank=True)
    # * invoice number with prefix
    invoice_number_full = models.CharField(max_length=32, null=True, blank=True)
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
        return (
            self.PaymentStatus.PAID
            if self.amount_due <= 0
            else self.PaymentStatus.PENDING
        )

    def calculate_total(self):
        return (self.subtotal - self.discount) + self.cgst + self.sgst

    @property
    def cgst_percent(self):
        return self.CGST_PERCENT if self.restaurant.gstin else 0.0

    @property
    def sgst_percent(self):
        return self.SGST_PERCENT if self.restaurant.gstin else 0.0

    def calculate_gst(self):
        amt = self.subtotal - self.discount
        self.cgst = amt * self.cgst_percent
        self.sgst = amt * self.sgst_percent

    def assign_invoice_number(self):
        if self.finalized and not self.invoice_number:
            self.invoice_number = (
                Invoice.objects.filter(
                    restaurant=self.restaurant, finalized=True
                ).count()
                + 1
            )
            self.invoice_number_full = (
                f"{self.restaurant.invoice_prefix}{self.invoice_number}"
            )

    def save(self, *args, **kwargs):
        self.calculate_gst()
        self.total = round(self.calculate_total(), 2)
        self.subtotal = round(self.subtotal, 2)
        self.cgst = round(self.cgst, 2)
        self.sgst = round(self.sgst, 2)
        self.assign_invoice_number()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_number}-{self.restaurant.name} - {self.finalized}"


class KOT(BaseFinanceModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)


class Order(BaseFinanceModel):
    class Size(models.TextChoices):
        HALF = "Half"
        FULL = "Full"

    dish = models.ForeignKey(Dish, on_delete=models.DO_NOTHING)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    kot = models.ForeignKey(KOT, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=16, choices=Size.choices, default=Size.FULL)
    cost = models.FloatField(default=0.0)
    dish_description = models.CharField(max_length=100, null=True, blank=True)
