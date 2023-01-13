from authentication.models import Restaurant
from finance.models import KOT, Invoice


class KOTService:
    def __init__(self, items: list, table: str, restaurant_id: str) -> None:
        self.items = items
        self.table = table
        self.restaurant = Restaurant.objects.get(id=restaurant_id)

    def create(self):
        invoice, _ = Invoice.objects.get_or_create(
            table=self.table, restaurant=self.restaurant, finalized=False
        )
        kot = KOT(invoice=invoice, items=self.items, restaurant=self.restaurant)
        kot.save()
        return kot
