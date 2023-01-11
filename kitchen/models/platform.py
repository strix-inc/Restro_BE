from django.db import models
from .base import BaseKitchenModel


class Platform(BaseKitchenModel):
    name = models.CharField(max_length=64)

    class Meta:
        unique_together = ("restaurant", "name")
