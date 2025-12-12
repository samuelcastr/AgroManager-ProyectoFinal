from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CultivoViewSet, CicloSiembraViewSet

router = DefaultRouter()
router.register(r'cultivos', CultivoViewSet, basename='cultivo')
router.register(r'ciclos', CicloSiembraViewSet, basename='ciclo')

urlpatterns = [
    path('', include(router.urls)),
    path('api/', include(router.urls)),
]
