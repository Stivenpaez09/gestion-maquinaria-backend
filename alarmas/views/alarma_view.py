from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from alarmas.serializers.alarma_serializer import AlarmaSerializer
from alarmas.services.alarma_service import AlarmaService
from alarmas.services.alarma_service_interface import IAlarmaService
from logins.permissions.rol_permissions import RolPermission


class AlarmaViewSet(viewsets.ModelViewSet):
    """
    ViewSet profesional para la gestión de alarmas.
    Gestiona listado, consulta individual y marcado como vista,
    manteniendo toda la lógica en el servicio (principios SOLID).
    """

    permission_key = "alarma"
    permission_classes = [RolPermission]

    def __init__(
        self,
        service: IAlarmaService = AlarmaService(),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.service = service

    # -------------------------------------------------------
    #                     LISTAR (GET)
    # -------------------------------------------------------
    def list(self, request, *args, **kwargs):
        """Retorna todas las alarmas registradas."""
        alarmas = self.service.listar_alarmas()
        serializer = AlarmaSerializer(alarmas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                OBTENER (GET/{id})
    # -------------------------------------------------------
    def retrieve(self, request, *args, **kwargs):
        """Retorna una alarma específica por ID."""
        pk = kwargs.get("pk")

        try:
            alarma = self.service.obtener_alarma(id_alarma=pk)
            serializer = AlarmaSerializer(alarma)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response(
                {"detail": "Alarma no encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

    # -------------------------------------------------------
    #      ENDPOINT PERSONALIZADO: MARCAR COMO VISTA
    # -------------------------------------------------------
    @action(detail=True, methods=['patch'], url_path='marcar-vista')
    def marcar_como_vista(self, request, pk=None):
        """
        Marca una alarma como vista.
        PATCH /alarmas/{id}/marcar-vista/
        """
        try:
            alarma = self.service.marcar_como_vista(id_alarma=pk)
            return Response(alarma, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response(
                {"detail": "Alarma no encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

    # -------------------------------------------------------
    #      ENDPOINT PERSONALIZADO: CANTIDAD NO VISTAS
    # -------------------------------------------------------
    @action(detail=False, methods=['get'], url_path='no-vistas')
    def cantidad_no_vistas(self, request):
        """
        Retorna la cantidad de alarmas que aún no han sido vistas.
        GET /alarmas/no-vistas/
        """
        try:
            cantidad = self.service.obtener_cantidad_alarmas_no_vistas()
            return Response(
                {"cantidad_no_vistas": cantidad},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                {"detail": "Error al obtener las alarmas no vistas."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

