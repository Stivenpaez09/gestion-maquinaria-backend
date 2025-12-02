from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from cursos.serializers.curso_serializer import CursoSerializer
from cursos.services.curso_service_interface import ICursoService
from cursos.services.curso_service import CursoService

class CursoViewSet(viewsets.ModelViewSet):
    """
    ViewSet profesional para la gestión de cursos.
    Gestiona listado, creación, consulta individual,
    actualización y eliminación, manteniendo la lógica
    en el servicio (principios SOLID).
    """

    def __init__(
        self,
        service: ICursoService = CursoService(),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.service = service

    # -------------------------------------------------------
    #                     LISTAR (GET)
    # -------------------------------------------------------
    def list(self, request, *args, **kwargs):
        """Retorna todos los cursos."""
        cursos = self.service.listar_cursos()
        serializer = CursoSerializer(cursos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                 OBTENER (GET/{id})
    # -------------------------------------------------------
    def retrieve(self, request, *args, **kwargs):
        """Retorna un curso por ID."""
        pk = kwargs.get("pk")
        curso = self.service.obtener_curso(id_curso=pk)

        if not curso:
            return Response(
                {"detail": "Curso no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CursoSerializer(curso)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                     CREAR (POST)
    # -------------------------------------------------------
    def create(self, request, *args, **kwargs):
        """Crea un curso usando el servicio."""
        try:
            curso = self.service.crear_curso(request.data)
            return Response(curso, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #               ACTUALIZAR (PUT/PATCH)
    # -------------------------------------------------------
    def update(self, request, *args, **kwargs):
        """Actualiza un curso existente."""
        pk = kwargs.get("pk")

        try:
            curso = self.service.actualizar_curso(
                id_curso=pk,
                data=request.data
            )
            return Response(curso, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #                     ELIMINAR (DELETE)
    # -------------------------------------------------------
    def destroy(self, request, *args, **kwargs):
        """Elimina un curso por ID."""
        pk = kwargs.get("pk")

        try:
            self.service.eliminar_curso(id_curso=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #     ENDPOINT PERSONALIZADO: CURSOS POR USUARIO
    # -------------------------------------------------------
    @action(detail=False, methods=['get'], url_path='usuario/(?P<id_usuario>[^/.]+)')
    def cursos_por_usuario(self, request, id_usuario=None):
        """
        Endpoint para obtener todos los cursos asociados a un usuario.
        GET /cursos/usuario/{id_usuario}/
        """
        cursos = self.service.obtener_cursos_por_usuario(id_usuario=id_usuario)
        serializer = CursoSerializer(cursos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
