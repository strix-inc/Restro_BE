from django.urls import path

from .views import DishView, PlatformView, CategoryView, StaffView

urlpatterns = [
    path("dish", DishView.as_view()),
    path("platform", PlatformView.as_view()),
    path("category", CategoryView.as_view()),
    path("staff", StaffView.as_view())
]
