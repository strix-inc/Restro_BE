from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from authentication.mixins import MemberAccessMixin

from authentication.services import SignupService
from .serializers import RestaurantSerializer


@method_decorator(csrf_exempt, name="dispatch")
class Signup(APIView):
    def post(self, request):
        """
        API to signup
        Request Body
        {
            "restaurant_name": "DAAWAT",
            "contact": "123",
            "password": "hello"
        }
        """
        data = request.data
        restaurant_name = data.get("restaurant_name")
        contact = data.get("contact")
        password = data.get("password")
        if not all([restaurant_name, contact, password]):
            return HttpResponseBadRequest(
                "Restaurant Name, Contact & Password should be present"
            )
        if SignupService.does_restaurant_name_exists(restaurant_name):
            return HttpResponseBadRequest("Restaurant Name already exists")

        if SignupService.does_phone_number_exists(contact):
            return HttpResponseBadRequest("Phone number already exists")

        signup_obj = SignupService(restaurant_name, contact, password)
        member = signup_obj.signup()
        response_data = {"user_id": member.user.id, "username": member.user.username}
        return JsonResponse(response_data)


class UniqueCheckerView(APIView):
    def get(self, request):
        params = request.query_params
        phone = params.get("contact")
        restaurant_name = params.get("restaurant_name")

        if restaurant_name and SignupService.does_restaurant_name_exists(
            restaurant_name
        ):
            return HttpResponseBadRequest("Restaurant Name already exists")

        if phone and SignupService.does_phone_number_exists(phone):
            return HttpResponseBadRequest("Phone number already exists")

        return HttpResponse("Ok!")


class RestaurantView(APIView, MemberAccessMixin):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        restaurant = self.get_restaurant(request)
        data = RestaurantSerializer(restaurant).data
        return JsonResponse({"data": data})

    def put(self, request):
        restaurant = self.get_restaurant(request)
        data = request.data
        serializer = RestaurantSerializer(restaurant, data=data)
        if not serializer.is_valid():
            return HttpResponseBadRequest(serializer.errors)
        serializer.save()
        return HttpResponse("Restaurant Details Updated", status=201)
