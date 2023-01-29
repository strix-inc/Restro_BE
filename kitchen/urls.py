from django.urls import path

from .views import DishView, PlatformView

urlpatterns = [
    path("dish", DishView.as_view()),
    path("platform", PlatformView.as_view()),
]
