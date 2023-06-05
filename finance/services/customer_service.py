from typing import Optional
from authentication.models.restaurant import Restaurant

from finance.models.sale import Customer


class CustomerService:
    def __init__(self, restaurant: Restaurant, contact: str, name: Optional[str] = None, gstin: Optional[str] = None) -> None:
        self.contact = contact
        self.restaurant = restaurant
        self.name = name
        self.gstin = gstin

    def get_customer(self) -> Customer:
        return Customer.objects.get(contact=self.contact, restaurant=self.restaurant)

    def create_or_update_customer(self) -> Customer:
        customer, _ = Customer.objects.get_or_create(contact=self.contact, restaurant=self.restaurant)

        customer.name = self.name
        customer.gstin = self.gstin
        customer.save()

        return customer
