from typing import Union
from uuid import UUID
from authentication.models.restaurant import Restaurant

from kitchen.models.food import Category, Dish, DishRate
from kitchen.models.platform import Platform
from kitchen.services.category_service import CategoryService


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

    def get_dish(self, name: str, category: Category, dish_type: Dish.DishType):
        dish, _ = Dish.objects.get_or_create(
            name=name.strip().upper(), category=category, restaurant=self.restaurant, dish_type=dish_type
        )
        return dish

    def create_new_dish(
        self, name: str, category_name: str, rates: list, dish_type: Dish.DishType
    ) -> Dish:
        category = CategoryService(self.restaurant).get_category(category_name)
        dish = self.get_dish(name, category, dish_type)
        self.add_dish_rates(dish, rates)
        return dish

    def update_dish(self, dish_id: Union[str, UUID], name: str, category_name: str, rates: list, dish_type: Dish.DishType) -> Dish:
        dish = Dish.objects.get(id=dish_id, restaurant=self.restaurant)
        category = CategoryService(self.restaurant).get_category(category_name)
        dish.name = name
        dish.category = category
        dish.dish_type = dish_type
        dish.save()
        self.add_dish_rates(dish, rates)
        return dish
