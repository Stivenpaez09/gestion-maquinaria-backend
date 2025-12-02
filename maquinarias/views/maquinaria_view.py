from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
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