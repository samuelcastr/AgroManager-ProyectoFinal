from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CultivoViewSet, TiposViewSet

router = DefaultRouter()
router.register(r'tipos', TiposViewSet, basename='tipos-cultivo')
router.register(r'cultivos', CultivoViewSet, basename='cultivos')

urlpatterns = [
    path('', include(router.urls)),
]