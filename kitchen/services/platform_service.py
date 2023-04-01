from authentication.models.restaurant import Restaurant
from kitchen.models.platform import Platform


class PlatformService:
    DEFAULT_PLATFORMS = ["Restaurant", "Zomato", "Swiggy"]

    def __init__(self, restaurant: Restaurant) -> None:
        self.restaurant = restaurant

    def create_defaults(self):
        for platform in self.DEFAULT_PLATFORMS:
            obj = Platform(name=platform, restaurant=self.restaurant)
            obj.save()
