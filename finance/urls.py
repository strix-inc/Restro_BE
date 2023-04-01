from django.urls import path

from .views import KOTView, InvoiceView, OrderView

urlpatterns = [
    path("kot", KOTView.as_view()),
    path("invoice", InvoiceView.as_view()),
    path("order", OrderView.as_view()),
]
