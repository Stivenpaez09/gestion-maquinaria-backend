from rest_framework.routers import DefaultRouter

from logins.views.login_view import LoginViewSet

router = DefaultRouter()
router.register(r'', LoginViewSet, basename='logins')

urlpatterns = router.urls