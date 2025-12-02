from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from usuarios.serializers.usuario_serializer import UsuarioSerializer
from usuarios.services.usuario_service_interface import IUsuarioService
from usuarios.services.usuario_service import UsuarioService

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet profesional para la gestión de usuarios.
    Gestiona listado, creación, consulta individual,
    actualización y eliminación, manteniendo la lógica
    en el servicio (principios SOLID).
    """

    def __init__(
        self,
        service: IUsuarioService = UsuarioService(),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.service = service

    # -------------------------------------------------------
    #                     LISTAR (GET)
    # -------------------------------------------------------
    def list(self, request, *args, **kwargs):
        """Retorna todos los usuarios."""
        usuarios = self.service.listar_usuarios()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                     OBTENER (GET/{id})
    # -------------------------------------------------------
    def retrieve(self, request, *args, **kwargs):
        """Retorna un usuario por ID."""
        pk = kwargs.get("pk")
        usuario = self.service.obtener_usuario(id_usuario=pk)

        if not usuario:
            return Response(
                {"detail": "Usuario no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                     CREAR (POST)
    # -------------------------------------------------------
    def create(self, request, *args, **kwargs):
        """
        Crea un nuevo usuario.
        Se maneja foto desde request.FILES.
        """

        data = request.data.copy()   # dict mutable
        # borrar completamente cualquier basura previa
        if "foto" in data:
            del data["foto"]

        foto = request.FILES.get("foto")
        if foto:
            data["foto"] = foto
        else:
            data["foto"] = None

        print("DEBUG REQUEST.DATA:", request.data)
        print("DEBUG REQUEST.FILES:", request.FILES)
        print("DEBUG DATA FINAL QUE SE ENVIA AL SERVICE:", data)

        try:
            usuario = self.service.crear_usuario(data)
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #                     ACTUALIZAR (PUT/PATCH)
    # -------------------------------------------------------
    def update(self, request, *args, **kwargs):
        """
        Actualiza un usuario existente.
        Maneja foto opcional.
        """
        pk = kwargs.get("pk")

        data = request.data.copy()
        data["foto"] = request.FILES.get("foto")  # puede venir o no

        try:
            usuario_actualizado = self.service.actualizar_usuario(
                id_usuario=pk,
                data=data
            )
            serializer = UsuarioSerializer(usuario_actualizado)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #                     ELIMINAR (DELETE)
    # -------------------------------------------------------
    def destroy(self, request, *args, **kwargs):
        """Elimina un usuario."""
        pk = kwargs.get("pk")

        try:
            self.service.eliminar_usuario(id_usuario=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
