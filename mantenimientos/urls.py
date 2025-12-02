
from rest_framework.routers import DefaultRouter
from mantenimientos.views.mantenimiento_view import MantenimientoViewSet

router = DefaultRouter()
router.register(r'', MantenimientoViewSet, basename='manteniemientos')

urlpatterns = router.urls