from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from logins.permissions.rol_permissions import RolPermission
from mantenimientos.serializers.mantenimiento_serializer import MantenimientoSerializer
from mantenimientos.services.mantenimiento_service import MantenimientoService
from mantenimientos.services.mantenimiento_service_interface import IMantenimientoService


class MantenimientoViewSet(viewsets.ModelViewSet):
    """
    ViewSet profesional para la gestión de mantenimientos.
    Gestiona listado, creación, consulta individual,
    actualización y eliminación, manteniendo la lógica
    en el servicio (principios SOLID).
    """

    permission_key = "mantenimiento"
    permission_classes = [RolPermission]

    def __init__(
        self,
        service: IMantenimientoService = MantenimientoService(),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.service = service

    # -------------------------------------------------------
    #                     LISTAR (GET)
    # -------------------------------------------------------
    def list(self, request, *args, **kwargs):
        """Retorna todos los mantenimientos."""
        mantenimientos = self.service.listar_mantenimientos()
        serializer = MantenimientoSerializer(mantenimientos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                     OBTENER (GET/{id})
    # -------------------------------------------------------
    def retrieve(self, request, *args, **kwargs):
        """Retorna un mantenimiento por ID."""
        pk = kwargs.get("pk")
        mantenimiento = self.service.obtener_mantenimiento(id_mantenimiento=pk)

        if not mantenimiento:
            return Response(
                {"detail": "Mantenimiento no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MantenimientoSerializer(mantenimiento)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                     CREAR (POST)
    # -------------------------------------------------------
    def create(self, request, *args, **kwargs):
        """Crea un mantenimiento usando el servicio."""
        try:
            data = self.service.crear_mantenimiento(request.data)
            return Response(data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #                     ACTUALIZAR (PUT/PATCH)
    # -------------------------------------------------------
    def update(self, request, *args, **kwargs):
        """Actualiza un mantenimiento existente."""
        pk = kwargs.get("pk")

        try:
            data = self.service.actualizar_mantenimiento(
                id_mantenimiento=pk,
                data=request.data
            )
            return Response(data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #                     ELIMINAR (DELETE)
    # -------------------------------------------------------
    def destroy(self, request, *args, **kwargs):
        """Elimina un mantenimiento."""
        pk = kwargs.get("pk")

        try:
            self.service.eliminar_mantenimiento(id_mantenimiento=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #          ENDPOINT PERSONALIZADO POR MÁQUINA
    # -------------------------------------------------------
    @action(detail=False, methods=['get'], url_path='maquina/(?P<id_maquina>[^/.]+)')
    def mantenimientos_por_maquina(self, request, id_maquina=None):
        """
        Endpoint para listar mantenimientos por máquina.
        GET /mantenimientos/maquina/{id_maquina}/
        """
        mantenimientos = self.service.obtener_mantenimientos_por_maquina(id_maquina)
        serializer = MantenimientoSerializer(mantenimientos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #          ENDPOINT PERSONALIZADO POR USUARIO
    # -------------------------------------------------------
    @action(detail=False, methods=['get'], url_path='usuario/(?P<id_usuario>[^/.]+)')
    def mantenimientos_por_usuario(self, request, id_usuario=None):
        """
        Endpoint para listar mantenimientos por usuario.
        GET /mantenimientos/usuario/{id_usuario}/
        """
        mantenimientos = self.service.obtener_mantenimientos_por_usuario(id_usuario)
        serializer = MantenimientoSerializer(mantenimientos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
