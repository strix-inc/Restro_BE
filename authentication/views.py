import json
from authentication.services.signup_service import SignupService

from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse
from django.views import View

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name="dispatch")
class Signup(View):
    def post(self, request):
        data = request.POST or json.loads(request.body)
        restaurant_name = data.get("restaurant_name")
        contact = data.get("contact")
        password = data.get("password")
        if not all([restaurant_name, contact, password]):
            return HttpResponseBadRequest("Restaurant Name, Contact & Password should be present")
        signup_obj = SignupService(restaurant_name, contact, password)
        member = signup_obj.signup()
        return HttpResponse("OK!")
