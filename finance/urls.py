from django.urls import path

from .views import KOTView

urlpatterns = [path("kot", KOTView.as_view())]
