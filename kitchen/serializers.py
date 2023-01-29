from rest_framework import serializers

from kitchen.models.food import Dish, DishRate


class DishRateSerializer(serializers.ModelSerializer):
    platform_name = serializers.CharField(source="platform.name")

    class Meta:
        model = DishRate
        fields = "__all__"


class DishSerializer(serializers.ModelSerializer):
    rates = serializers.SerializerMethodField("dish_rates")
    category_name = serializers.CharField(source="category.name")

    def dish_rates(self, dish):
        rates = DishRate.objects.filter(dish=dish)
        serializer = DishRateSerializer(rates, many=True)
        return serializer.data

    class Meta:
        model = Dish
        fields = "__all__"