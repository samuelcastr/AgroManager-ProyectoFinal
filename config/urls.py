from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from config.swagger import schema_view

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import permissions

from apps.core.views import (
    RegisterAPIView,
    RequestPasswordResetAPIView,
    ConfirmPasswordResetAPIView,
    CustomTokenObtainPairView,
)

urlpatterns = [
    # -----------------------
    # Admin
    # -----------------------
    path("admin/", admin.site.urls),

    # -----------------------
    # Core API
    # -----------------------
    path("api/core/", include("apps.core.urls")),

    # -----------------------
    # Autenticación JWT
    # -----------------------
    path(
        "api/auth/login/",
        csrf_exempt(CustomTokenObtainPairView.as_view()),
        name="token_obtain_pair",
    ),
    path(
        "api/auth/refresh/",
        csrf_exempt(TokenRefreshView.as_view()),
        name="token_refresh",
    ),
    path(
        "api/auth/register/",
        csrf_exempt(RegisterAPIView.as_view()),
        name="register",
    ),
    path(
        "api/auth/password-reset/",
        csrf_exempt(RequestPasswordResetAPIView.as_view()),
        name="password_reset_request",
    ),
    path(
        "api/auth/password-reset-confirm/",
        csrf_exempt(ConfirmPasswordResetAPIView.as_view()),
        name="password_reset_confirm",
    ),

    # -----------------------
    # Apps adicionales
    # -----------------------
    path('api/inventario/', include('apps.inventario.urls')),
    path('api/cultivos/', include('apps.cultivos.urls')),
    path('api/sensores/', include('apps.sensores.urls')),
    path('api/datainspector/', include('apps.datainspector.urls')),

    # -----------------------
    # Swagger & Redoc
    # -----------------------
    # Permite Swagger en producción, con permisos seguros si se desea
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger-ui"
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="redoc-ui"
    ),
    path(
        "swagger.json",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json"
    ),
]

