from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from proyectos.serializers.proyecto_serializer import ProyectoSerializer
from proyectos.services.proyecto_service_interface import IProyectoService
from proyectos.services.proyecto_service import ProyectoService

class ProyectoViewSet(viewsets.ModelViewSet):
    """
    ViewSet profesional para la gestión de proyectos.
    Gestiona listado, creación, consulta individual,
    actualización y eliminación, delegando la lógica
    al servicio correspondiente (principios SOLID).
    """

    def __init__(
        self,
        service: IProyectoService = ProyectoService(),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.service = service

    # -------------------------------------------------------
    #                     LISTAR (GET)
    # -------------------------------------------------------
    def list(self, request, *args, **kwargs):
        """Retorna todos los proyectos registradas."""
        proyectos = self.service.listar_proyectos()
        serializer = ProyectoSerializer(proyectos, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                 OBTENER (GET/{id})
    # -------------------------------------------------------
    def retrieve(self, request, *args, **kwargs):
        """Retorna un proyecto por ID."""
        pk = kwargs.get("pk")
        proyecto = self.service.obtener_proyecto(id_proyecto=pk)

        if not proyecto:
            return Response(
                {"detail": "Proyecto no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProyectoSerializer(proyecto).data
        return Response(serializer, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                     CREAR (POST)
    # -------------------------------------------------------
    def create(self, request, *args, **kwargs):
        """Crea un nuevo proyecto usando el servicio."""
        try:
            proyecto = self.service.crear_proyecto(request.data)
            serializer = ProyectoSerializer(proyecto).data
            return Response(serializer, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #               ACTUALIZAR (PUT/PATCH)
    # -------------------------------------------------------
    def update(self, request, *args, **kwargs):
        """Actualiza un proyecto existente."""
        pk = kwargs.get("pk")

        try:
            proyecto = self.service.actualizar_proyecto(
                id_proyecto=pk,
                data=request.data
            )
            serializer = ProyectoSerializer(proyecto).data
            return Response(serializer, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #                     ELIMINAR (DELETE)
    # -------------------------------------------------------
    def destroy(self, request, *args, **kwargs):
        """Elimina un proyecto por ID."""
        pk = kwargs.get("pk")

        try:
            self.service.eliminar_proyecto(id_proyecto=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #      LISTAR PROYECTOS POR EMPRESA (GET ?empresa=ID)
    # -------------------------------------------------------
    @action(detail=False, methods=["get"], url_path="por-empresa/(?P<id_empresa>[^/.]+)")
    def listar_por_empresa(self, request, id_empresa=None):
        """
        Retorna todos los proyectos asociados a una empresa específica.
        Uso:
            GET /api/proyectos/por-empresa/1
        """

        proyectos = self.service.listar_proyectos_por_empresa(id_empresa)
        serializer = ProyectoSerializer(proyectos, many=True).data

        return Response(serializer, status=status.HTTP_200_OK)