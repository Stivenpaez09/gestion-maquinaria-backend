from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from conductores.serializers.conductor_serializer import ConductorSerializer
from conductores.services.conductor_service import ConductorService
from conductores.services.conductor_service_interface import IConductorService
from logins.permissions.rol_permissions import RolPermission


class ConductorViewSet(viewsets.ModelViewSet):
    """
    ViewSet profesional para la gestión de conductores.
    Gestiona listado, creación, consulta individual,
    actualización y eliminación, manteniendo la lógica
    en el servicio (principios SOLID).
    """

    permission_key = "conductor"
    permission_classes = [RolPermission]

    def __init__(
        self,
        service: IConductorService = ConductorService(),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.service = service

    # -------------------------------------------------------
    #                     LISTAR (GET)
    # -------------------------------------------------------
    def list(self, request, *args, **kwargs):
        """Retorna todos los conductores."""
        conductores = self.service.listar_conductores()
        serializer = ConductorSerializer(conductores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                 OBTENER (GET/{id})
    # -------------------------------------------------------
    def retrieve(self, request, *args, **kwargs):
        """Retorna un conductor por ID."""
        pk = kwargs.get("pk")
        conductor = self.service.obtener_conductor(id_conductor=pk)

        if not conductor:
            return Response(
                {"detail": "Conductor no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ConductorSerializer(conductor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                     CREAR (POST)
    # -------------------------------------------------------
    def create(self, request, *args, **kwargs):
        """Crea un conductor usando el servicio."""
        try:
            conductor = self.service.crear_conductor(request.data)
            return Response(conductor, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #               ACTUALIZAR (PUT/PATCH)
    # -------------------------------------------------------
    def update(self, request, *args, **kwargs):
        """Actualiza un conductor existente."""
        pk = kwargs.get("pk")

        try:
            conductor = self.service.actualizar_conductor(
                id_conductor=pk,
                data=request.data
            )
            return Response(conductor, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #                     ELIMINAR (DELETE)
    # -------------------------------------------------------
    def destroy(self, request, *args, **kwargs):
        """Elimina un conductor por ID."""
        pk = kwargs.get("pk")

        try:
            self.service.eliminar_conductor(id_conductor=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
