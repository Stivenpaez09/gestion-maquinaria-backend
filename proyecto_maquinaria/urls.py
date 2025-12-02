from rest_framework.routers import DefaultRouter

from proyecto_maquinaria.views.proyecto_maquinaria_view import ProyectoMaquinariaViewSet

router = DefaultRouter()
router.register(r'', ProyectoMaquinariaViewSet, basename='proyecto_maquinaria')

urlpatterns = router.urls