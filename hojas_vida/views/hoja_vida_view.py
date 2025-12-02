from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from hojas_vida.serializers.hoja_vida_serializer import HojaVidaSerializer
from hojas_vida.services.hoja_vida_service import HojaVidaService
from hojas_vida.services.hoja_vida_service_interface import IHojaVidaService


class HojaVidaViewSet(viewsets.ModelViewSet):
    """
    ViewSet profesional para la gestión de hojas de vida.
    Gestiona listado, creación, consulta individual,
    actualización y eliminación, manteniendo la lógica
    en el servicio (principios SOLID).
    """

    def __init__(
        self,
        service: IHojaVidaService = HojaVidaService(),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.service = service

    # -------------------------------------------------------
    #                     LISTAR (GET)
    # -------------------------------------------------------
    def list(self, request, *args, **kwargs):
        """Retorna todas las hojas de vida registradas."""
        hojas = self.service.listar_hojas_vida()
        serializer = HojaVidaSerializer(hojas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                     OBTENER (GET/{id})
    # -------------------------------------------------------
    def retrieve(self, request, *args, **kwargs):
        """Retorna una hoja de vida por ID."""
        pk = kwargs.get("pk")
        hoja = self.service.obtener_hoja_vida(id_hoja=pk)

        serializer = HojaVidaSerializer(hoja)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                     CREAR (POST)
    # -------------------------------------------------------
    def create(self, request, *args, **kwargs):
        """
        Crea una nueva hoja de vida.
        Se maneja archivo desde request.FILES.
        """
        data = request.data.copy()  # dict mutable
        data["archivo"] = request.FILES.get("archivo")  # adjuntar archivo

        try:
            hoja = self.service.crear_hoja_vida(data)
            serializer = HojaVidaSerializer(hoja)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #                     ACTUALIZAR (PUT/PATCH)
    # -------------------------------------------------------
    def update(self, request, *args, **kwargs):
        """
        Actualiza una hoja de vida existente.
        Maneja archivo opcional.
        """
        pk = kwargs.get("pk")
        data = request.data.copy()
        data["archivo"] = request.FILES.get("archivo")  # puede venir o no

        try:
            hoja_actualizada = self.service.actualizar_hoja_vida(
                id_hoja=pk,
                data=data
            )
            serializer = HojaVidaSerializer(hoja_actualizada)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #                     ELIMINAR (DELETE)
    # -------------------------------------------------------
    def destroy(self, request, *args, **kwargs):
        """Elimina una hoja de vida por ID."""
        pk = kwargs.get("pk")

        try:
            self.service.eliminar_hoja_vida(id_hoja=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)