from rest_framework import serializers

from .models import KOT

class KOTSerializer(serializers.ModelSerializer):
    class Meta:
        model = KOT
        fields = ["items", "id"]
