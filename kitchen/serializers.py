from rest_framework import serializers

from kitchen.models.food import Dish, DishRate, Category
from kitchen.models.platform import Platform


class DishRateSerializer(serializers.ModelSerializer):
    platform_name = serializers.CharField(source="platform.name")

    class Meta:
        model = DishRate
        fields = "__all__"


class DishSerializer(serializers.ModelSerializer):
    rates = DishRateSerializer(read_only=True, many=True)
    category_name = serializers.CharField(source="category.name")

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
