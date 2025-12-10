from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlertasStockAPIView, AjusteMasivoAPIView, InsumoViewSet, LoteViewSet, MovimientoStockViewSet

router = DefaultRouter()
router.register(r'insumos', InsumoViewSet, basename='insumo')
router.register(r'lotes', LoteViewSet, basename='lote')
router.register(r'movimientos', MovimientoStockViewSet, basename='movimiento')

urlpatterns = [
    path("", include(router.urls)),
    path("alertas-stock/", AlertasStockAPIView.as_view(), name="alertas-stock"),
    path("ajuste-masivo/", AjusteMasivoAPIView.as_view(), name="ajuste-masivo"),
]
