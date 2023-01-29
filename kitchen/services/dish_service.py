from authentication.models.restaurant import Restaurant

from kitchen.models.food import Category, Dish, DishRate
from kitchen.models.platform import Platform


class DishService:
    @classmethod
    def create_new_dish(
        cls, name: str, category: str, rates: list, restaurant: Restaurant
    ):
        category, _ = Category.objects.get_or_create(
            name=category, restaurant=restaurant
        )
        dish, _ = Dish.objects.get_or_create(
            name=name, category=category, restaurant=restaurant
        )

        for rate in rates:
            platform = Platform.objects.get(id=rate["platform"], restaurant=restaurant)
            dish_rate, _ = DishRate.objects.get_or_create(
                dish=dish, restaurant=restaurant, platform=platform
            )
            dish_rate.half_price = rate["half_price"]
            dish_rate.full_price = rate["full_price"]
            dish_rate.save()

        return dish
