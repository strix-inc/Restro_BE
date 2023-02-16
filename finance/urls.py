from django.urls import path

from .views import KOTView, InvoiceView

urlpatterns = [path("kot", KOTView.as_view()), path("invoice", InvoiceView.as_view())]
