from authentication.models.restaurant import Restaurant
from kitchen.models.food import Category


class CategoryService:
    DEFAULT_CATEGORIES = ["Starter", "Main Course", "Dessert"]

    def __init__(self, restaurant: Restaurant) -> None:
        self.restaurant = restaurant

    def create_defaults(self):
        for category in self.DEFAULT_CATEGORIES:
            obj = Category(name=category, restaurant=self.restaurant)
            obj.save()

    def get_category(self, name):
        category, _ = Category.objects.get_or_create(
            name=name.strip().upper(), restaurant=self.restaurant
        )
        return category
