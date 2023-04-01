from django.db import models
from restrofin.base_model import BaseModel


class Restaurant(BaseModel):
    class Country(models.TextChoices):
        INDIA = "India"

    # * Legal
    name = models.CharField(max_length=256, unique=True)
    gstin = models.CharField(max_length=32, blank=True, null=True)
    fssai_number = models.CharField(max_length=32, null=True, blank=True)

    # * Address
    address_street = models.CharField(max_length=256, blank=True, null=True)
    address_city = models.CharField(max_length=256, blank=True, null=True)
    address_state = models.CharField(max_length=256, blank=True, null=True)
    address_country = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        choices=Country.choices,
        default=Country.INDIA,
    )

    # * Info
    logo = models.ImageField(null=True, blank=True)
    contact = models.CharField(max_length=32, null=True, blank=True)
    display_name = models.CharField(max_length=256, null=True, blank=True)
    upi_id = models.CharField(max_length=256, null=True, blank=True)
    invoice_prefix = models.CharField(max_length=16, default="INV-")

    def __str__(self) -> str:
        return self.name
