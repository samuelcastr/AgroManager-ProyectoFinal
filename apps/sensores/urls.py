from rest_framework.routers import DefaultRouter
from .views import SensorViewSet, LecturaViewSet, TiposViewSet

router = DefaultRouter()
router.register('tipos', TiposViewSet, basename='tipos-sensor')
router.register('sensores', SensorViewSet)
router.register('lecturas', LecturaViewSet, basename='lecturas')

urlpatterns = router.urls
