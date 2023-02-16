from distutils.util import strtobool
from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from authentication.mixins import MemberAccessMixin
from finance.models.sale import KOT, Invoice
from finance.services.invoice_service import InvoiceService

from .serializers import InvoiceSerializer, KOTSerializer
from .services.kot_service import KOTService


class BaseView(APIView, MemberAccessMixin):
    permission_classes = (IsAuthenticated,)


class KOTView(BaseView):
    def get(self, request):
        restaurant = self.get_restaurant(request)
        kot_id = request.query_params.get("id")

        if kot_id:
            try:
                kot = KOT.objects.get(id=kot_id, restaurant=restaurant)
            except KOT.DoesNotExist:
                return HttpResponseNotFound("KOT does not exist")
            else:
                return JsonResponse({"data": KOTSerializer(kot).data})

        kots = KOT.objects.filter(restaurant=restaurant)

        invoice_id = request.query_params.get("invoice_id")
        finalized = strtobool(request.query_params.get("finalized", "false"))
        if invoice_id:
            kots = kots.filter(invoice_id=invoice_id)

        invoices = Invoice.objects.filter(restaurant=restaurant, finalized=finalized)
        kots = kots.filter(invoice__in=invoices)

        kots = kots.order_by("-created_at")
        serializer = KOTSerializer(kots, many=True)
        return JsonResponse({"data": serializer.data})

    def post(self, request):
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
        restaurant = self.get_restaurant(request)

        data = request.data
        items = data.get("items", [])
        table = data.get("table")

        if not all([items, table]):
            return HttpResponseBadRequest("items & table are required values")

        kot = KOTService(items=items, table=table, restaurant=restaurant).create()
        return JsonResponse({"data": KOTSerializer(kot).data})


class InvoiceView(BaseView):
    def get(self, request):
        restaurant = self.get_restaurant(request)
        invoice_id = request.query_params.get("id")
        if invoice_id:
            try:
                invoice = Invoice.objects.get(id=invoice_id, restaurant=restaurant)
            except Invoice.DoesNotExist:
                return HttpResponseNotFound("Invoice Does Not Exist")
            else:
                serializer = InvoiceSerializer(invoice)
                return JsonResponse({"data": serializer.data})

        finalized = strtobool(request.query_params.get("finalized", "true"))
        invoices = Invoice.objects.filter(
            restaurant=restaurant, finalized=finalized
        ).order_by("-created_at")
        serializer = InvoiceSerializer(invoices, many=True)
        return JsonResponse({"data": serializer.data})

    def put(self, request):
        """
        {
            "id": "xajcnanl",
            "discount": 100.0,
            "subtotal": 200.0,
            "platform": "platform_id_123"
            "orders": [
                {
                    "id": "123",
                    "dish_id": "xyz",
                    "quantity": 2,
                    "size": "half",
                }
            ]
        }
        """
        restaurant = self.get_restaurant(request)
        data = request.data
        invoice = InvoiceService(
            invoice_id=data["id"],
            platform_id=data["platform"],
            restaurant=restaurant,
            orders=data["orders"],
            subtotal=data["subtotal"],
            discount=data["discount"],
        ).update_invoice()
        serializer = InvoiceSerializer(invoice)
        return JsonResponse({"data": serializer.data}, status=201)
