from rest_framework import routers
from hojas_vida.views.hoja_vida_view import HojaVidaViewSet

router = routers.DefaultRouter()
router.register(r'', HojaVidaViewSet, basename='hojas_vida')
urlpatterns = router.urls