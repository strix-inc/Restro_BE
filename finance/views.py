from collections import Counter
from datetime import datetime
from distutils.util import strtobool
from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
)
from django.db.models import Max, Avg

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from authentication.mixins import MemberAccessMixin
from finance.models.sale import KOT, Invoice, Order
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
    def _get_top_selling_and_lowest_selling_item(self, invoices):
        top, bottom = "", ""
        if not invoices:
            return top, bottom

        orders = Order.objects.filter(invoice__in=invoices)
        if not orders:
            return top, bottom

        dishes = orders.values_list("dish__name", flat=True)
        if not dishes:
            return top, bottom
        counts = Counter(dishes)
        sorted_dishes = sorted(counts.items(), key=lambda x: x[1])
        top, bottom = sorted_dishes[-1][0], sorted_dishes[0][0]
        return top, bottom

    def _get_one_invoice(self, invoice_id, restaurant):
        try:
            invoice = Invoice.objects.get(id=invoice_id, restaurant=restaurant)
        except Invoice.DoesNotExist:
            return HttpResponseNotFound("Invoice Does Not Exist")
        else:
            serializer = InvoiceSerializer(invoice)
            return JsonResponse({"data": serializer.data})

    def get(self, request):
        restaurant = self.get_restaurant(request)
        invoice_id = request.query_params.get("id")
        if invoice_id:
            return self._get_one_invoice(invoice_id, restaurant)

        finalized = strtobool(request.query_params.get("finalized", "true"))
        invoices = Invoice.objects.filter(
            restaurant=restaurant, finalized=finalized, is_deleted=False
        )

        if not finalized:
            # * Active invoices/tables
            invoices = invoices.order_by("-created_at")
            serializer = InvoiceSerializer(invoices, many=True)
            return JsonResponse({"data": serializer.data})

        start_date = request.query_params.get("from") or datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        if start_date:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%d/%m/%Y")
            invoices = invoices.filter(created_at__gte=start_date)

        end_date = request.query_params.get("to")
        if end_date:
            end_date = datetime.strptime(end_date, "%d/%m/%Y")
            invoices = invoices.filter(created_at__lte=end_date)

        payment_type = request.query_params.get("payment")
        if payment_type:
            invoices = invoices.filter(payment_type=payment_type)

        platform = request.query_params.get("platform")
        if platform:
            invoices = invoices.filter(platform__name=platform)

        invoices = invoices.order_by("-created_at")
        serializer = InvoiceSerializer(invoices, many=True)

        max_sale = invoices.aggregate(Max("total"))["total__max"] or 0.0
        average_sale = invoices.aggregate(Avg("total"))["total__avg"] or 0.0
        (
            top_selling_item,
            lowest_selling_item,
        ) = self._get_top_selling_and_lowest_selling_item(invoices)
        return JsonResponse(
            {
                "data": serializer.data,
                "max_sale": max_sale,
                "avg_sale": average_sale,
                "highest_selling_item": top_selling_item,
                "lowest_selling_item": lowest_selling_item,
            }
        )

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

    def delete(self, request):
        restaurant = self.get_restaurant(request)
        data = request.data
        invoice_id = data["id"]
        # ! Hard Delete only if the invoice hasn't been finalized
        Invoice.objects.filter(
            id=invoice_id, restaurant=restaurant, finalized=False
        ).delete()
        Invoice.objects.filter(
            id=invoice_id, restaurant=restaurant, finalized=True
        ).update(is_deleted=True)

        return JsonResponse(
            {"data": f"Invoice with ID {invoice_id} deleted"}, status=200
        )


class OrderView(BaseView):
    def delete(self, request):
        restaurant = self.get_restaurant(request)
        data = request.data
        order_id = data["id"]
        Order.objects.filter(id=order_id, restaurant=restaurant).delete()
        return JsonResponse({"data": f"Order with ID {order_id} deleted"}, status=200)
