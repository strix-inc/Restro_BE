from typing import Optional, Union
from uuid import UUID
from authentication.models.restaurant import Restaurant

from finance.models.sale import Invoice, Order, Customer
from kitchen.models.food import DishRate
from kitchen.models.platform import Platform
from kitchen.models.staff import Staff


class InvoiceService:
    def __init__(
        self,
        invoice_id: Union[str, UUID],
        platform_id: Union[UUID, str],
        restaurant: Restaurant,
        orders: Optional[list] = None,
        subtotal: float = 0.0,
        discount: float = 0.0,
        delivery_charge: float = 0.0,
        staff_id: Union[str, UUID] = None,
        customer: Optional[Customer] = None,
    ) -> None:
        if orders is None:
            orders = []
        self.invoice = Invoice.objects.get(id=invoice_id)
        self.restaurant = restaurant
        self.orders = orders
        self.subtotal = subtotal
        self.discount = discount
        self.delivery_charge = delivery_charge
        self.platform = Platform.objects.get(id=platform_id)
        self.staff = Staff.objects.get(id=staff_id) if staff_id else None
        self.customer = customer

    def update_customer(self, customer_phone, customer_name):
        customer = Customer.objects.get_or_create(contact=customer_phone.strip())
        customer.name = customer_name
        customer.save()
        return customer

    def _update_order(self, order_id: Union[UUID, str], order_details: dict) -> dict:
        quantity = order_details["quantity"]
        size = order_details["size"]
        dish_id = order_details["dish"]
        rate = DishRate.objects.get(
            dish_id=dish_id, platform=self.platform, restaurant=self.restaurant
        )
        if size == Order.Size.FULL:
            cost = rate.full_price
        elif size == Order.Size.HALF:
            cost = rate.half_price
        Order.objects.filter(id=order_id, restaurant=self.restaurant).update(
            quantity=quantity, size=size, cost=cost
        )

    def update_orders(self):
        id_set = set()
        for order in self.orders:
            order_id = order["id"]
            self._update_order(order_id=order_id, order_details=order)
            id_set.add(order_id)

        # ! delete the items that were removed from the list
        Order.objects.filter(invoice=self.invoice, restaurant=self.restaurant).exclude(
            id__in=id_set
        ).delete()

    def update_invoice(self):
        self.update_orders()
        self.invoice.platform = self.platform
        self.invoice.subtotal = self.subtotal
        self.invoice.discount = self.discount
        self.invoice.delivery_charge = self.delivery_charge
        self.invoice.staff = self.staff
        self.invoice.customer = self.customer
        if not self.invoice.finalized:
            self.invoice.finalized = True
        self.invoice.save()
        return self.invoice
