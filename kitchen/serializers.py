from rest_framework import serializers

from kitchen.models.food import Dish, DishRate, Category
from kitchen.models.platform import Platform
from kitchen.models.staff import Staff


class DishRateSerializer(serializers.ModelSerializer):
    platform_name = serializers.CharField(source="platform.name")

    class Meta:
        model = DishRate
        fields = "__all__"


class DishSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name")

    def dish_rates(self, dish):
        rates = DishRate.objects.select_related("dish").filter(dish=dish)
        serializer = DishRateSerializer(rates, many=True)
        return serializer.data

    class Meta:
        model = Dish
        fields = "__all__"


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = "__all__"
