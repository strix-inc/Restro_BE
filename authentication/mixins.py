from django.contrib.auth.models import User

from authentication.models import Restaurant, Member

class MemberAccessMixin:
    @classmethod
    def is_authorized_for_restaurant(cls, user: User, restaurant_id: str) -> bool:
        return Member.objects.filter(user=user, restaurant=restaurant_id).exists()
