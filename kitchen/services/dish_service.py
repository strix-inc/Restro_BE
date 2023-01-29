from typing import Union
from uuid import UUID
from authentication.models.restaurant import Restaurant

from kitchen.models.food import Category, Dish, DishRate
from kitchen.models.platform import Platform


class DishService:
    def __init__(self, restaurant: Restaurant) -> None:
        self.restaurant = restaurant

    def add_dish_rates(self, dish: Dish, rates: list):
        for rate in rates:
            platform = Platform.objects.get(id=rate["platform"], restaurant=self.restaurant)
            dish_rate, _ = DishRate.objects.get_or_create(
                dish=dish, restaurant=self.restaurant, platform=platform
            )
            dish_rate.half_price = rate["half_price"]
            dish_rate.full_price = rate["full_price"]
            dish_rate.save()

    def create_new_dish(
        self, name: str, category: str, rates: list, dish_type: Dish.DishType
    ) -> Dish:
        category, _ = Category.objects.get_or_create(
            name=category, restaurant=self.restaurant
        )
        dish, _ = Dish.objects.get_or_create(
            name=name, category=category, restaurant=self.restaurant, dish_type=dish_type
        )
        self.add_dish_rates(dish, rates)
        return dish

    def update_dish(self, dish_id: Union[str, UUID], name: str, category: str, rates: list, dish_type: Dish.DishType) -> Dish:
        dish = Dish.objects.get(id=dish_id, restaurant=self.restaurant)
        category, _ = Category.objects.get_or_create(
            name=category, restaurant=self.restaurant
        )
        dish.name = name
        dish.category = category
        dish.dish_type = dish_type
        dish.save()
        self.add_dish_rates(dish, rates)
        return dish
