import json

from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse

from rest_framework.views import APIView

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from authentication.services import SignupService


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
        data = json.loads(request.body)
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
