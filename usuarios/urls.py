from rest_framework.routers import DefaultRouter
from .views.usuario_view import UsuarioViewSet

router = DefaultRouter()
router.register(r'', UsuarioViewSet, basename='usuarios')

urlpatterns = router.urls