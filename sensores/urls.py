from rest_framework.routers import DefaultRouter
from .views import SensorViewSet, LecturaViewSet

router = DefaultRouter()
router.register('sensores', SensorViewSet)
router.register('lecturas', LecturaViewSet, basename='lecturas')

urlpatterns = router.urls
