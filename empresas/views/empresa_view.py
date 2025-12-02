from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from empresas.serializers.empresa_serializer import EmpresaSerializer
from empresas.services.empresa_service import EmpresaService
from empresas.services.empresa_service_interface import IEmpresaService


class EmpresaViewSet(viewsets.ModelViewSet):
    """
    ViewSet profesional para la gestión de empresas.
    Gestiona listado, creación, consulta individual,
    actualización y eliminación, delegando la lógica
    de negocio al servicio correspondiente (principios SOLID).
    """

    def __init__(
        self,
        service: IEmpresaService = EmpresaService(),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.service = service

    # -------------------------------------------------------
    #                     LISTAR (GET)
    # -------------------------------------------------------
    def list(self, request, *args, **kwargs):
        """Retorna todas las empresas."""
        empresas = self.service.listar_empresas()
        serializer = EmpresaSerializer(empresas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                 OBTENER (GET/{id})
    # -------------------------------------------------------
    def retrieve(self, request, *args, **kwargs):
        """Retorna una empresa por ID."""
        pk = kwargs.get("pk")

        try:
            empresa = self.service.obtener_empresa(id_empresa=pk)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmpresaSerializer(empresa)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                     CREAR (POST)
    # -------------------------------------------------------
    def create(self, request, *args, **kwargs):
        """Crea una empresa usando el servicio."""
        try:
            empresa = self.service.crear_empresa(request.data)
            serializer = EmpresaSerializer(empresa)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(e.message_dict if hasattr(e, "message_dict") else str(e),
                            status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #               ACTUALIZAR (PUT/PATCH)
    # -------------------------------------------------------
    def update(self, request, *args, **kwargs):
        """Actualiza una empresa existente."""
        pk = kwargs.get("pk")

        try:
            empresa = self.service.actualizar_empresa(id_empresa=pk, data=request.data)
            serializer = EmpresaSerializer(empresa)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(e.message_dict if hasattr(e, "message_dict") else str(e),
                            status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #                     ELIMINAR (DELETE)
    # -------------------------------------------------------
    def destroy(self, request, *args, **kwargs):
        """Elimina una empresa por ID."""
        pk = kwargs.get("pk")

        try:
            self.service.eliminar_empresa(id_empresa=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)