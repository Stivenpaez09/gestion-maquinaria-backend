from rest_framework.routers import DefaultRouter

from proyectos.views.proyecto_view import ProyectoViewSet

router = DefaultRouter()
router.register(r'', ProyectoViewSet, basename='proyectos')

urlpatterns = router.urls