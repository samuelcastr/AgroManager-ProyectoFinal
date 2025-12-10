"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from config.swagger import schema_view

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.core.views import register, request_password_reset, confirm_password_reset

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Core API
    path("api/core/", include("apps.core.urls")),

    # Autenticación JWT
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/register/", register, name="register"),
    path("api/auth/password-reset/", request_password_reset, name="password_reset_request"),
    path("api/auth/password-reset-confirm/", confirm_password_reset, name="password_reset_confirm"),
    path('inventario/', include('apps.inventario.urls')),
    path('api/inventario/', include('apps.inventario.urls')),
    path('api/cultivos', include('cultivos.urls')),
    path('api/sensores', include('sensores.urls')),

    # Swagger
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-ui"),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),

]

