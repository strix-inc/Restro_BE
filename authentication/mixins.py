from django.contrib.auth.models import User

from authentication.models import Restaurant, Member


class MemberAccessMixin:
    @classmethod
    def is_authorized_for_restaurant(cls, user: User, restaurant_id: str) -> bool:
        return Member.objects.filter(user=user, restaurant=restaurant_id).exists()

    @classmethod
    def is_request_authorised_for_restaurant(cls, request, restaurant_id: str) -> bool:
        user = request.user
        return cls.is_authorized_for_restaurant(user, restaurant_id)

    @classmethod
    def get_member(cls, request):
        user = request.user
        return Member.objects.get(user=user)

    @classmethod
    def get_restaurant(cls, request):
        member = cls.get_member(request)
        return member.restaurant
