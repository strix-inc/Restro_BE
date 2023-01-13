from django.urls import path

from .views import KOTView

urlpatterns = [path("<str:restaurant_id>/kot", KOTView.as_view())]
