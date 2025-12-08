from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from logins.permissions.rol_permissions import RolPermission
from maquinarias.serializers.maquinaria_serializer import MaquinariaSerializer
from maquinarias.services.maquinaria_service import MaquinariaService
from maquinarias.services.maquinaria_service_interface import IMaquinariaService

class MaquinariaViewSet(viewsets.ModelViewSet):
    """
    ViewSet profesional para la gestión de maquinarias.
    Gestiona listado, creación, consulta individual,
    actualización y eliminación, manteniendo la lógica
    en el servicio (principios SOLID).
    """

    permission_key = "maquinaria"
    permission_classes = [RolPermission]

    def __init__(
        self,
        service: IMaquinariaService = MaquinariaService(),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.service = service

    # -------------------------------------------------------
    #                     LISTAR (GET)
    # -------------------------------------------------------
    def list(self, request, *args, **kwargs):
        """Retorna todas las maquinarias."""
        maquinarias = self.service.listar_maquinarias()
        serializer = MaquinariaSerializer(maquinarias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                 OBTENER (GET/{id})
    # -------------------------------------------------------
    def retrieve(self, request, *args, **kwargs):
        """Retorna una maquinaria por ID."""
        pk = kwargs.get("pk")
        maquinaria = self.service.obtener_maquinaria(id_maquina=pk)

        if not maquinaria:
            return Response(
                {"detail": "Maquinaria no encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MaquinariaSerializer(maquinaria)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                     CREAR (POST)
    # -------------------------------------------------------
    def create(self, request, *args, **kwargs):
        """Crea una maquinaria usando el servicio."""
        try:
            maquinaria = self.service.crear_maquinaria(request.data)
            serializer = MaquinariaSerializer(maquinaria)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #               ACTUALIZAR (PUT/PATCH)
    # -------------------------------------------------------
    def update(self, request, *args, **kwargs):
        """Actualiza una maquinaria existente."""
        pk = kwargs.get("pk")

        try:
            maquinaria = self.service.actualizar_maquinaria(
                id_maquina=pk,
                data=request.data
            )
            serializer = MaquinariaSerializer(maquinaria)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #                     ELIMINAR (DELETE)
    # -------------------------------------------------------
    def destroy(self, request, *args, **kwargs):
        """Elimina una maquinaria por ID."""
        pk = kwargs.get("pk")

        try:
            self.service.eliminar_maquinaria(id_maquina=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #            RESUMEN DE MAQUINARIAS (GET /resumen)
    # -------------------------------------------------------
    @action(detail=False, methods=['get'], url_path='resumen')
    def resumen_maquinarias(self, request):
        """
        Retorna un resumen consolidado del estado de todas las máquinas.
        
        GET /api/maquinarias/resumen/
        
        Response:
        {
            "en_operacion": int,
            "al_dia": int,
            "pendientes": int,
            "vencidos": int
        }
        """
        try:
            resumen = self.service.obtener_resumen_maquinarias()
            return Response(resumen, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {"detail": f"Error al generar resumen: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # -------------------------------------------------------
    #     MAQUINARIAS EN OPERACION (GET /maquinarias/en-operacion)
    # ------------------------------------------------------
    @action(detail=False, methods=['get'], url_path='en-operacion')
    def maquinarias_en_operacion(self, request):
        """
        Retorna las maquinarias actualmente en operación.
        GET /api/maquinarias/en-operacion/
        """
        try:
            maquinarias = self.service.obtener_maquinarias_operacion()
            serializer = MaquinariaSerializer(maquinarias, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"detail": f"Error al obtener maquinarias en operación: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # -------------------------------------------------------
    #     MAQUINARIAS EN OPERACION (GET /maquinarias/vencidas)
    # ------------------------------------------------------
    @action(detail=False, methods=['get'], url_path='vencidas')
    def maquinarias_vencidas(self, request):
        """
        Retorna maquinarias con mantenimiento vencido.
        GET /api/maquinarias/vencidas/
        """
        try:
            maquinarias = self.service.obtener_maquinarias_vencidas()
            serializer = MaquinariaSerializer(maquinarias, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"detail": f"Error al obtener maquinarias vencidas: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # -------------------------------------------------------
    #     MAQUINARIAS EN OPERACION (GET /maquinarias/pendientes)
    # ------------------------------------------------------
    @action(detail=False, methods=['get'], url_path='pendientes')
    def maquinarias_pendientes(self, request):
        """
        Retorna maquinarias que están próximas a vencer (entre 1 y 20 horas).
        GET /api/maquinarias/pendientes/
        """
        try:
            maquinarias = self.service.obtener_maquinarias_pendientes()
            serializer = MaquinariaSerializer(maquinarias, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"detail": f"Error al obtener maquinarias pendientes: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # -------------------------------------------------------
    #     MAQUINARIAS EN OPERACION (GET /maquinarias/al-dia)
    # ------------------------------------------------------
    @action(detail=False, methods=['get'], url_path='al-dia')
    def maquinarias_al_dia(self, request):
        """
        Retorna maquinarias con mantenimiento al día.
        GET /api/maquinarias/al-dia/
        """
        try:
            maquinarias = self.service.obtener_maquinarias_al_dia()
            serializer = MaquinariaSerializer(maquinarias, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"detail": f"Error al obtener maquinarias al día: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='ultimas-maquinarias')
    def ultimas_maquinarias(self, request):
        """
        Retorna maquinarias con mantenimiento al día.
        GET /api/maquinarias/al-dia/
        """
        try:
            maquinarias = self.service.listar_ultimas_maquinarias()
            serializer = MaquinariaSerializer(maquinarias, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"detail": f"Error al obtener las ultimas maquinarias: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
