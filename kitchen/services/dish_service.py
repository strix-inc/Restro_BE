from typing import Union
from uuid import UUID
from authentication.models.restaurant import Restaurant

from kitchen.models.food import Category, Dish, DishRate
from kitchen.models.platform import Platform


class DishService:
    @classmethod
    def add_dish_rates(cls, dish: Dish, rates: list, restaurant: Restaurant):
        for rate in rates:
            platform = Platform.objects.get(id=rate["platform"], restaurant=restaurant)
            dish_rate, _ = DishRate.objects.get_or_create(
                dish=dish, restaurant=restaurant, platform=platform
            )
            dish_rate.half_price = rate["half_price"]
            dish_rate.full_price = rate["full_price"]
            dish_rate.save()

    @classmethod
    def create_new_dish(
        cls, name: str, category: str, rates: list, restaurant: Restaurant
    ) -> Dish:
        category, _ = Category.objects.get_or_create(
            name=category, restaurant=restaurant
        )
        dish, _ = Dish.objects.get_or_create(
            name=name, category=category, restaurant=restaurant
        )
        cls.add_dish_rates(dish, rates, restaurant)
        return dish

    @classmethod
    def update_dish(cls, dish_id: Union[str, UUID], name: str, category: str, rates: list, restaurant: Restaurant) -> Dish:
        dish = Dish.objects.get(id=dish_id, restaurant=restaurant)
        category, _ = Category.objects.get_or_create(
            name=category, restaurant=restaurant
        )
        dish.name = name
        dish.category = category
        dish.save()
        cls.add_dish_rates(dish, rates, restaurant)
        return dish
