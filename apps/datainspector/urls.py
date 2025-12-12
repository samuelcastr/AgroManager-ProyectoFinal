from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ExportExcelSelectViewSet, ExportGlobalExcelViewSet

router = DefaultRouter()
router.register(r'export/excel', ExportExcelSelectViewSet, basename='export_excel_select')
router.register(r'export/global_excel', ExportGlobalExcelViewSet, basename='export_global_excel')

urlpatterns = router.urls
