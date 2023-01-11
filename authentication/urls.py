from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import Signup, UniqueCheckerView

urlpatterns = [
    path("signup", Signup.as_view()),
    path("unique-checker", UniqueCheckerView.as_view()),
    path(
        "login/token", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "login/token/refresh",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
