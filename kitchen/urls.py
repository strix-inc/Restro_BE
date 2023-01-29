from django.urls import path

from .views import DishView

urlpatterns = [path("dish", DishView.as_view())]
