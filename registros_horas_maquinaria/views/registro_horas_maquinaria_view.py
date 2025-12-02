from functools import partial

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from registros_horas_maquinaria.serializers.registro_horas_maquinaria_serializer import \
    RegistroHorasMaquinariaSerializer
from registros_horas_maquinaria.services.registro_horas_maquinaria_service import RegistroHorasMaquinariaService
from registros_horas_maquinaria.services.registro_horas_maquinaria_service_interface import \
    IRegistroHorasMaquinariaService
from usuarios.serializers.usuario_serializer import UsuarioSerializer


class RegistroHorasMaquinariaViewSet(viewsets.ModelViewSet):
    """
    ViewSet profesional para la gestión de registros de horas de maquinaria.
    Gestiona:
    - Listado completo
    - Consulta individual
    - Creación
    - Actualización
    - Eliminación
    Todo delegando la lógica de negocio al servicio correspondiente.
    """

    def __init__(
        self,
        service: IRegistroHorasMaquinariaService = RegistroHorasMaquinariaService(),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.service = service

    # -------------------------------------------------------
    #                     LISTAR (GET)
    # -------------------------------------------------------
    def list(self, request, *args, **kwargs):
        """Retorna todos los registros de horas de maquinaria."""
        registros = self.service.listar_registros()
        serializer = RegistroHorasMaquinariaSerializer(registros, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                     OBTENER (GET/{id})
    # -------------------------------------------------------
    def retrieve(self, request, *args, **kwargs):
        """Retorna un registro de horas por ID."""
        pk = kwargs.get("pk")
        registro = self.service.obtener_registro(id_registro=pk)

        serializer = RegistroHorasMaquinariaSerializer(registro)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                     CREAR (POST)
    # -------------------------------------------------------
    def create(self, request, *args, **kwargs):
        """
        Crea un registro de horas.
        Usa serializer + lógica del servicio.
        """
        try:
            data = self.service.crear_registro(request.data)
            return Response(data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #                     ACTUALIZAR (PUT/PATCH)
    # -------------------------------------------------------
    def update(self, request, *args, **kwargs):
        """Actualiza un registro de horas existente."""
        pk = kwargs.get("pk")

        try:
            data = self.service.actualizar_registro(
                id_registro=pk,
                data=request.data
            )
            return Response(data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #                     ELIMINAR (DELETE)
    # -------------------------------------------------------
    def destroy(self, request, *args, **kwargs):
        """Elimina un registro de horas por ID."""
        pk = kwargs.get("pk")

        try:
            self.service.eliminar_registro(id_registro=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #     ENDPOINT PERSONALIZADO: Registros por Máquina
    # -------------------------------------------------------
    @action(detail=False, methods=['get'], url_path='maquina/(?P<id_maquina>[^/.]+)')
    def registros_por_maquina(self, request, id_maquina=None):
        """
        GET /registro-horas/maquina/{id_maquina}/
        Obtiene todos los registros de horas asociados a una máquina.
        """
        registros = self.service.obtener_por_maquina(id_maquina)
        serializer = RegistroHorasMaquinariaSerializer(registros, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)