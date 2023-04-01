from django.urls import path

from .views import DishView, PlatformView, CategoryView

urlpatterns = [
    path("dish", DishView.as_view()),
    path("platform", PlatformView.as_view()),
    path("category", CategoryView.as_view()),
]
