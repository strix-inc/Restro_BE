from django.urls import path
from .views import Signup, UniqueCheckerView

urlpatterns = [
    path("signup", Signup.as_view()),
    path("unique-checker", UniqueCheckerView.as_view()),
]
