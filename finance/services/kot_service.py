from authentication.models import Restaurant
from finance.models import KOT, Invoice, Order
from kitchen.models.food import Dish


class KOTService:
    def __init__(self, items: list, table: str, restaurant: Restaurant) -> None:
        self.items = items
        self.table = table
        self.restaurant = restaurant

    def create_items(self, kot: KOT):
        objects = [
            Order(
                dish_id=item["id"],
                restaurant=self.restaurant,
                kot=kot,
                invoice=kot.invoice,
                quantity=item["quantity"],
                size=item["size"],
                dish_description=Dish.objects.get(id=item["id"]).name
            )
            for item in self.items
        ]
        Order.objects.bulk_create(objects)

    def create(self):
        invoice, _ = Invoice.objects.get_or_create(
            table=self.table, restaurant=self.restaurant, finalized=False
        )
        kot = KOT(invoice=invoice, restaurant=self.restaurant)
        kot.save()
        self.create_items(kot)
        return kot
