from authentication.models.member import Member
from authentication.models.restaurant import Restaurant
from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password


class SignupService:
    def __init__(self, restaurant_name: str, phone: str, password: str) -> None:
        self.restaurant_name = restaurant_name.strip()
        self.phone = phone.strip()
        self.password = password.strip()

    def create_user(self):
        password = make_password(self.password)
        user = User(username=self.phone, password=password)
        user.save()
        return user

    def create_restaurant(self):
        restaurant = Restaurant(
            name=self.restaurant_name,
            display_name=self.restaurant_name,
            contact=self.phone,
        )
        restaurant.save()
        return restaurant

    def create_member(self, user: User, restaurant: Restaurant):
        member = Member(user=user, restaurant=restaurant)
        member.save()
        return member

    def signup(self) -> Member:
        user = self.create_user()
        restaurant = self.create_restaurant()
        return self.create_member(user, restaurant)

    @classmethod
    def does_restaurant_name_exists(cls, restaurant_name: str) -> bool:
        return Restaurant.objects.filter(name=restaurant_name).exists()

    @classmethod
    def does_phone_number_exists(cls, contact: str) -> bool:
        return User.objects.filter(username=contact).exists()
