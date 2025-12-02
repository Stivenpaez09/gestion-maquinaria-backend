from rest_framework.routers import DefaultRouter
from .views.maquinaria_view import MaquinariaViewSet

router = DefaultRouter()
router.register(r'', MaquinariaViewSet, basename="maquinarias")

urlpatterns = router.urls