from collections import OrderedDict
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from authentication.mixins import MemberAccessMixin
from kitchen.serializers import DishSerializer
from kitchen.services.dish_service import DishService
from .models.food import Dish, DishRate


class DishView(APIView, MemberAccessMixin):
    permission_classes = (IsAuthenticated,)

    def _group_into_categories(self, dishes: list) -> dict:
        category_map = OrderedDict()
        for dish in dishes:
            category_name = dish["category_name"]
            category_dishes = category_map.get(category_name, [])
            category_dishes.append(dish)
            category_map[category_name] = category_dishes

        return category_map

    def get(self, request):
        dish_id = request.query_params.get("id")
        restaurant = self.get_restaurant(request)

        if dish_id:
            try:
                dish = Dish.objects.get(id=dish_id, restaurant=restaurant)
            except Dish.DoesNotExist:
                return HttpResponseNotFound("No Dish Found")
            else:
                dish_serializer = DishSerializer(dish)
                return JsonResponse({"data": dish_serializer.data})

        dishes = Dish.objects.filter(restaurant=restaurant)
        dish_serializer = DishSerializer(dishes, many=True)
        return JsonResponse({"data": self._group_into_categories(dish_serializer.data)})

    def post(self, request):
        """
        {
            "rates": [
                {
                    "half_price": 0.0,
                    "full_price": 0.0,
                    "platform": "426640aa-3c02-43f2-9f5e-f813cdb087ca"
                },
                {
                    "half_price": 0.0,
                    "full_price": 0.0,
                    "platform": "426640aa-3c02-43f2-9f5e-f813cdb087ca"
                }
            ],
            "name": "chicken",
            "category": "RICE"
        }
        """
        restaurant = self.get_restaurant(request)
        data = request.data
        dish = DishService(restaurant=restaurant).create_new_dish(
            name=data["name"],
            category=data["category"],
            rates=data["rates"]
        )
        dish_serializer = DishSerializer(dish)
        return JsonResponse({"data": dish_serializer.data}, status=201)

    def put(self, request):
        restaurant = self.get_restaurant(request)
        data = request.data
        dish = DishService(restaurant=restaurant).update_dish(
            dish_id=data["id"],
            name=data["name"],
            category=data["category"],
            rates=data["rates"]
        )
        dish_serializer = DishSerializer(dish)
        return JsonResponse({"data": dish_serializer.data}, status=201)

    def delete(self, request):
        restaurant = self.get_restaurant(request)
        data = request.data
        try:
            dish = Dish.objects.get(id=data["id"], restaurant=restaurant)
        except Dish.DoesNotExist:
            return HttpResponseNotFound("Dish Not Found")
        else:
            DishRate.objects.filter(dish=dish).delete()
            dish.delete()
            return HttpResponse("Dish Deleted")
