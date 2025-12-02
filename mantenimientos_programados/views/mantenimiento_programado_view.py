from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from mantenimientos_programados.serializers.mantenimiento_programado_serializer import MantenimientoProgramadoSerializer
from mantenimientos_programados.services.mantenimiento_programado_service import MantenimientoProgramadoService
from mantenimientos_programados.services.mantenimiento_programado_service_interface import IMantenimientoProgramadoService

class MantenimientoProgramadoViewSet(viewsets.ModelViewSet):
    """
    ViewSet profesional para la gestión de mantenimientos programados.
    Gestiona listado, creación, consulta individual,
    actualización y eliminación, manteniendo la lógica
    en el servicio (principios SOLID).
    """

    def __init__(
        self,
        service: IMantenimientoProgramadoService = MantenimientoProgramadoService(),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.service = service

    # -------------------------------------------------------
    #                     LISTAR (GET)
    # -------------------------------------------------------
    def list(self, request, *args, **kwargs):
        """Retorna todos los mantenimientos programados."""
        mantenimientos = self.service.listar_mantenimientos_programados()
        serializer = MantenimientoProgramadoSerializer(mantenimientos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                OBTENER (GET/{id})
    # -------------------------------------------------------
    def retrieve(self, request, *args, **kwargs):
        """Retorna un mantenimiento programado por ID."""
        pk = kwargs.get("pk")
        mantenimiento = self.service.obtener_mantenimiento_programado(id_programado=pk)

        if not mantenimiento:
            return Response(
                {"detail": "Mantenimiento programado no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MantenimientoProgramadoSerializer(mantenimiento)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                     CREAR (POST)
    # -------------------------------------------------------
    def create(self, request, *args, **kwargs):
        """Crea un mantenimiento programado usando el servicio."""
        try:
            mantenimiento = self.service.crear_mantenimiento_programado(request.data)
            return Response(mantenimiento, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #               ACTUALIZAR (PUT/PATCH)
    # -------------------------------------------------------
    def update(self, request, *args, **kwargs):
        """Actualiza un mantenimiento programado existente."""
        pk = kwargs.get("pk")

        try:
            mantenimiento = self.service.actualizar_mantenimiento_programado(
                id_programado=pk,
                data=request.data
            )
            return Response(mantenimiento, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #                     ELIMINAR (DELETE)
    # -------------------------------------------------------
    def destroy(self, request, *args, **kwargs):
        """Elimina un mantenimiento programado por ID."""
        pk = kwargs.get("pk")

        try:
            self.service.eliminar_mantenimiento_programado(id_programado=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #     ENDPOINT PERSONALIZADO: POR MÁQUINA
    # -------------------------------------------------------
    @action(detail=False, methods=['get'], url_path='maquina/(?P<id_maquina>[^/.]+)')
    def mantenimientos_por_maquina(self, request, id_maquina=None):
        """
        Endpoint para obtener todos los mantenimientos programados
        asociados a una máquina específica.
        GET /mantenimientos-programados/maquina/{id_maquina}/
        """
        mantenimientos = self.service.obtener_mantenimientos_por_maquina(
            id_maquina=id_maquina
        )

        serializer = MantenimientoProgramadoSerializer(mantenimientos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

