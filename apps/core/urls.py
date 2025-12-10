from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.core.views import health, UserProfileViewSet, UnidadProductivaViewSet, AuditLogViewSet

# Router para ViewSets
router = DefaultRouter()
router.register('profiles', UserProfileViewSet, basename='userprofile')
router.register('unidades-productivas', UnidadProductivaViewSet, basename='unidadproductiva')
router.register('audit-logs', AuditLogViewSet, basename='auditlog')

urlpatterns = [
    # Health check
    path('health/', health, name='health-check'),
    
    # Router
    path('', include(router.urls)),
]
