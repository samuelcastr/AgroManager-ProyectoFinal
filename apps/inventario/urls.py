from django.urls import path
from .views import AlertasStockAPIView, AjusteMasivoAPIView

urlpatterns = [
    path("alertas-stock/", AlertasStockAPIView.as_view(), name="alertas-stock"),
    path("ajuste-masivo/", AjusteMasivoAPIView.as_view(), name="ajuste-masivo"),
]
