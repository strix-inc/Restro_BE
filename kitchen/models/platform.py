from django.db import models
from .base import BaseKitchenModel


class Platform(BaseKitchenModel):
    name = models.CharField(max_length=64)

    class Meta:
        unique_together = ("restaurant", "name")

    def __str__(self) -> str:
        return f"{self.name} ({self.restaurant.name})"

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.strip().upper()
        super().save()
