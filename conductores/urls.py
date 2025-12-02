from rest_framework.routers import DefaultRouter
from .views.conductor_view import ConductorViewSet

router = DefaultRouter()
router.register(r'', ConductorViewSet, basename='conductores')

urlpatterns = router.urls