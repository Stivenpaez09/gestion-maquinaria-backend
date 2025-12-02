from rest_framework.routers import DefaultRouter

from empresas.views.empresa_view import EmpresaViewSet

router = DefaultRouter()
router.register(r'', EmpresaViewSet, basename='empresas')

urlpatterns = router.urls