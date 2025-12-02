from rest_framework.routers import DefaultRouter
from alarmas.views.alarma_view import AlarmaViewSet

router = DefaultRouter()
router.register(r'', AlarmaViewSet, basename='alarmas')

urlpatterns = router.urls