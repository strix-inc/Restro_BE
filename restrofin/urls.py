from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
    path("finance/", include("finance.urls")),
    path("kitchen/", include("kitchen.urls")),
]
