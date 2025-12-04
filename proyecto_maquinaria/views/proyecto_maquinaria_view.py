from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from logins.permissions.rol_permissions import RolPermission
from proyecto_maquinaria.serializers.proyecto_maquinaria_serializer import ProyectoMaquinariaSerializer
from proyecto_maquinaria.services.proyecto_maquinaria_service import ProyectoMaquinariaService
from proyecto_maquinaria.services.proyecto_maquinaria_service_interface import IProyectoMaquinariaService


class ProyectoMaquinariaViewSet(viewsets.ModelViewSet):
    """
    ViewSet profesional para la gestión de asignaciones de máquinas a proyectos.
    Gestiona listado, creación, consulta individual,
    actualización y eliminación, manteniendo la lógica
    en el servicio (principios SOLID).
    """

    permission_key = "proyecto_maquinaria"
    permission_classes = [RolPermission]

    def __init__(
        self,
        service: IProyectoMaquinariaService = ProyectoMaquinariaService(),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.service = service

    # -------------------------------------------------------
    #                     LISTAR (GET)
    # -------------------------------------------------------
    def list(self, request, *args, **kwargs):
        """Retorna todas las asignaciones."""
        asignaciones = self.service.listar_asignaciones()
        serializer = ProyectoMaquinariaSerializer(asignaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                     OBTENER (GET/{id})
    # -------------------------------------------------------
    def retrieve(self, request, *args, **kwargs):
        """Retorna una asignación por ID."""
        pk = kwargs.get("pk")
        asignacion = self.service.obtener_asignacion(id_proyecto_maquinaria=pk)

        if not asignacion:
            return Response(
                {"detail": "Asignación no encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProyectoMaquinariaSerializer(asignacion)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                     CREAR (POST)
    # -------------------------------------------------------
    def create(self, request, *args, **kwargs):
        """Crea una asignación usando el servicio."""
        try:
            data = self.service.crear_asignacion(request.data)
            return Response(data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #                     ACTUALIZAR (PUT/PATCH)
    # -------------------------------------------------------
    def update(self, request, *args, **kwargs):
        """Actualiza una asignación existente."""
        pk = kwargs.get("pk")

        try:
            data = self.service.actualizar_asignacion(
                id_proyecto_maquinaria=pk,
                data=request.data
            )
            return Response(data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #                     ELIMINAR (DELETE)
    # -------------------------------------------------------
    def destroy(self, request, *args, **kwargs):
        """Elimina una asignación."""
        pk = kwargs.get("pk")

        try:
            self.service.eliminar_asignacion(id_proyecto_maquinaria=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #          ENDPOINT PERSONALIZADO POR PROYECTO
    # -------------------------------------------------------
    @action(detail=False, methods=['get'], url_path='proyecto/(?P<id_proyecto>[^/.]+)')
    def asignaciones_por_proyecto(self, request, id_proyecto=None):
        """
        Endpoint para listar asignaciones por proyecto.
        GET /proyecto_maquinaria/proyecto/{id_proyecto}/
        """
        asignaciones = self.service.listar_asignaciones()
        asignaciones = [a for a in asignaciones if a.proyecto.id_proyecto == int(id_proyecto)]
        serializer = ProyectoMaquinariaSerializer(asignaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #          ENDPOINT PERSONALIZADO POR MÁQUINA
    # -------------------------------------------------------
    @action(detail=False, methods=['get'], url_path='maquina/(?P<id_maquina>[^/.]+)')
    def asignaciones_por_maquina(self, request, id_maquina=None):
        """
        Endpoint para listar asignaciones por máquina.
        GET /proyecto_maquinaria/maquina/{id_maquina}/
        """
        asignaciones = self.service.listar_asignaciones()
        asignaciones = [a for a in asignaciones if a.maquina.id_maquina == int(id_maquina)]
        serializer = ProyectoMaquinariaSerializer(asignaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)