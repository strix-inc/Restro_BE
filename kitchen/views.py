from collections import OrderedDict
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from authentication.mixins import MemberAccessMixin
from kitchen.models.platform import Platform
from kitchen.serializers import DishSerializer, PlatformSerializer, CategorySerializer
from kitchen.services.dish_service import DishService
from .models.food import Dish, DishRate, Category


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
                dish = Dish.objects.get(id=dish_id, restaurant=restaurant, is_deleted=False)
            except Dish.DoesNotExist:
                return HttpResponseNotFound("No Dish Found")
            else:
                dish_serializer = DishSerializer(dish)
                return JsonResponse({"data": dish_serializer.data})

        dishes = Dish.objects.filter(restaurant=restaurant, is_deleted=False)
        dish_serializer = DishSerializer(dishes, many=True)
        return JsonResponse({"data": dish_serializer.data})

    def _get_dish_type(self, dish_type: str) -> Dish.DishType:
        return (
            Dish.DishType.VEG if dish_type.lower() == "veg" else Dish.DishType.NON_VEG
        )

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
            category_name=data["category"],
            rates=data["rates"],
            dish_type=self._get_dish_type(dish_type=data["dish_type"]),
        )
        dish_serializer = DishSerializer(dish)
        return JsonResponse({"data": dish_serializer.data}, status=201)

    def put(self, request):
        restaurant = self.get_restaurant(request)
        data = request.data
        dish = DishService(restaurant=restaurant).update_dish(
            dish_id=data["id"],
            name=data["name"],
            category_name=data["category"],
            rates=data["rates"],
            dish_type=self._get_dish_type(dish_type=data["dish_type"]),
        )
        dish_serializer = DishSerializer(dish)
        return JsonResponse({"data": dish_serializer.data}, status=200)

    def delete(self, request):
        restaurant = self.get_restaurant(request)
        data = request.data
        try:
            dish = Dish.objects.get(id=data["id"], restaurant=restaurant)
        except Dish.DoesNotExist:
            return HttpResponseNotFound("Dish Not Found")
        else:
            DishRate.objects.filter(dish=dish).update(is_deleted=True)
            dish.is_deleted = True
            dish.save()
            return HttpResponse("Dish Deleted")


class PlatformView(APIView, MemberAccessMixin):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        platform_id = request.query_params.get("id")
        restaurant = self.get_restaurant(request)

        if platform_id:
            try:
                platform = Platform.objects.get(id=platform_id, restaurant=restaurant)
            except Platform.DoesNotExist:
                return HttpResponseNotFound("No Dish Found")
            else:
                serializer = PlatformSerializer(platform)
                return JsonResponse({"data": serializer.data})

        platforms = Platform.objects.filter(restaurant=restaurant)
        serializer = PlatformSerializer(platforms, many=True)
        return JsonResponse({"data": serializer.data})

    def post(self, request):
        restaurant = self.get_restaurant(request)
        data = request.data
        name = data["name"]
        platform, _ = Platform.objects.get_or_create(
            name=name.strip().upper(), restaurant=restaurant
        )
        serializer = PlatformSerializer(platform)
        return JsonResponse({"data": serializer.data}, status=201)

    def put(self, request):
        restaurant = self.get_restaurant(request)
        data = request.data
        platform_id = data["id"]
        name = data["name"]
        try:
            platform = Platform.objects.get(id=platform_id, restaurant=restaurant)
        except Platform.DoesNotExist:
            return HttpResponseNotFound("Platform Not Found")
        else:
            platform.name = name
            platform.save()
            serializer = PlatformSerializer(platform)
            return JsonResponse({"data": serializer.data}, status=200)

    def delete(self, request):
        restaurant = self.get_restaurant(request)
        data = request.data
        platform_id = data["id"]
        try:
            platform = Platform.objects.get(id=platform_id, restaurant=restaurant)
        except Platform.DoesNotExist:
            return HttpResponseNotFound("Platform Not Found")
        else:
            platform.delete()
            return HttpResponse("Platform Deleted")


class CategoryView(APIView, MemberAccessMixin):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        category_id = request.query_params.get("id")
        restaurant = self.get_restaurant(request)

        if category_id:
            try:
                category = Category.objects.get(id=category_id, restaurant=restaurant)
            except Category.DoesNotExist:
                return HttpResponseNotFound("No Category Found")
            else:
                serializer = CategorySerializer(category)
                return JsonResponse({"data": serializer.data})

        categories = Category.objects.filter(restaurant=restaurant)
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse({"data": serializer.data})

    def post(self, request):
        restaurant = self.get_restaurant(request)
        data = request.data
        name = data["name"]
        category, _ = Category.objects.get_or_create(
            name=name.strip().upper(), restaurant=restaurant
        )
        serializer = CategorySerializer(category)
        return JsonResponse({"data": serializer.data}, status=201)

    def put(self, request):
        restaurant = self.get_restaurant(request)
        data = request.data
        category_id = data["id"]
        name = data["name"]
        try:
            category = Category.objects.get(id=category_id, restaurant=restaurant)
        except Category.DoesNotExist:
            return HttpResponseNotFound("Platform Not Found")
        else:
            category.name = name
            category.save()
            serializer = CategorySerializer(category)
            return JsonResponse({"data": serializer.data}, status=200)

    def delete(self, request):
        restaurant = self.get_restaurant(request)
        data = request.data
        category_id = data["id"]
        try:
            category = Category.objects.get(id=category_id, restaurant=restaurant)
        except Category.DoesNotExist:
            return HttpResponseNotFound("Platform Not Found")
        else:
            category.delete()
            return HttpResponse("Category Deleted")
