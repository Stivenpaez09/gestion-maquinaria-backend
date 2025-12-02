from rest_framework.routers import DefaultRouter

from registros_horas_maquinaria.views.registro_horas_maquinaria_view import RegistroHorasMaquinariaViewSet

router = DefaultRouter()
router.register(r'', RegistroHorasMaquinariaViewSet, basename='registros_horas_maquinaria')

urlpatterns = router.urls