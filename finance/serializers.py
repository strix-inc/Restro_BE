from rest_framework import serializers

from .models import KOT


class KOTSerializer(serializers.ModelSerializer):
    table = serializers.CharField(source="invoice.table")

    class Meta:
        model = KOT
        fields = ["items", "id", "table"]
