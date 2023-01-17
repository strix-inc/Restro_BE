from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from authentication.mixins import MemberAccessMixin
from finance.models.sale import KOT

from .serializers import KOTSerializer
from .services.kot_service import KOTService


class KOTView(APIView, MemberAccessMixin):
    permission_classes = (IsAuthenticated,)

    def get(self, request, restaurant_id: str):
        user = request.user
        is_valid_member = self.is_authorized_for_restaurant(user, restaurant_id)
        if not is_valid_member:
            return HttpResponseForbidden("Invalid Member for the restaurant")

        kot_id = request.query_params.get("id")

        if not kot_id:
            return HttpResponseBadRequest("kot_id param is missing")
        try:
            kot = KOT.objects.get(id=kot_id, restaurant_id=restaurant_id)
        except KOT.DoesNotExist:
            return HttpResponseNotFound("KOT does not exist")
        return JsonResponse({"data": KOTSerializer(kot).data})

    def post(self, request, restaurant_id: str):
        """
        Request Body
        {
            "table": "1",
            "items": [
                {
                    "id": "xyz",
                    "name": "Chicken",
                    "quantity": 2,
                    "size": "Half / Full"
                }
            ]
        }
        """
        user = request.user
        is_valid_member = self.is_authorized_for_restaurant(user, restaurant_id)
        if not is_valid_member:
            return HttpResponseForbidden("Invalid Member for the restaurant")

        data = request.data
        items = data.get("items", [])
        table = data.get("table")

        if not all([items, table]):
            return HttpResponseBadRequest("items & table are required values")

        kot = KOTService(items=items, table=table, restaurant_id=restaurant_id).create()

        return JsonResponse({"data": KOTSerializer(kot).data})
