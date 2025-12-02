from rest_framework.routers import DefaultRouter
from mantenimientos_programados.views.mantenimiento_programado_view import MantenimientoProgramadoViewSet

router = DefaultRouter()
router.register(r'', MantenimientoProgramadoViewSet, basename='mantenimientos_programados')

urlpatterns = router.urls