from authentication.models import Restaurant
from finance.models import KOT, Invoice


class KOTService:
    def __init__(self, items: list, table: str, restaurant: Restaurant) -> None:
        self.items = items
        self.table = table
        self.restaurant = restaurant

    def create(self):
        invoice, _ = Invoice.objects.get_or_create(
            table=self.table, restaurant=self.restaurant, finalized=False
        )
        kot = KOT(invoice=invoice, items=self.items, restaurant=self.restaurant)
        kot.save()
        return kot
