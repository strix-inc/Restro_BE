from rest_framework import serializers

from .models import KOT, Invoice, Order


class KOTSerializer(serializers.ModelSerializer):
    table = serializers.CharField(source="invoice.table")

    rates = serializers.SerializerMethodField("kot_orders")

    def kot_orders(self, kot):
        orders = Order.objects.filter(kot=kot)
        serializer = OrderSerializer(orders, many=True)
        return serializer.data

    class Meta:
        model = KOT
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    rates = serializers.SerializerMethodField("invoice_orders")

    def invoice_orders(self, invoice):
        orders = Order.objects.filter(invoice=invoice)
        serializer = OrderSerializer(orders, many=True)
        return serializer.data

    class Meta:
        model = Invoice
        fields = "__all__"
