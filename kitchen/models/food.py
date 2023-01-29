from django.db import models
from .base import BaseKitchenModel
from .platform import Platform


class Category(BaseKitchenModel):
    name = models.CharField(max_length=64)

    class Meta:
        unique_together = ("restaurant", "name")

    def __str__(self) -> str:
        return f"{self.name} ({self.restaurant.name})"


class Dish(BaseKitchenModel):
    class Unit(models.TextChoices):
        PLATE = "plate"

    name = models.CharField(max_length=32)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    unit = models.CharField(max_length=64, choices=Unit.choices, default=Unit.PLATE)

    class Meta:
        unique_together = ("restaurant", "name", "category")

    def __str__(self) -> str:
        return f"{self.name} ({self.restaurant.name})"


class DishRate(BaseKitchenModel):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    half_price = models.FloatField(default=0.0)
    full_price = models.FloatField(default=0.0)
    platform = models.ForeignKey(Platform, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ("restaurant", "dish", "platform")

    def __str__(self) -> str:
        return f"{self.dish.name} - {self.platform.name} ({self.restaurant.name})"
