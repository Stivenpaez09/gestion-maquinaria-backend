from rest_framework.routers import DefaultRouter
from cursos.views.curso_view import CursoViewSet

router = DefaultRouter()
router.register(r'', CursoViewSet, basename='cursos')

urlpatterns = router.urls

