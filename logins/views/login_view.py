from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from logins.permissions.rol_permissions import RolPermission
from logins.serializers.login_detail_serializer import LoginDetailSerializer
from logins.serializers.login_response_serializer import LoginResponseSerializer
from logins.services.login_service import LoginService
from logins.services.login_service_interface import ILoginService
from usuarios.serializers.usuario_serializer import UsuarioSerializer


class LoginViewSet(viewsets.ModelViewSet):
    """
    ViewSet profesional para la gestión de logins (credenciales).
    Mantiene los principios SOLID delegando la lógica al servicio.
    Proporciona:
    - Registro de credenciales
    - Autenticación (login)
    - CRUD (opcional)
    """
    permission_key = "login"
    permission_classes = [RolPermission]
    def __init__(
        self,
        service: ILoginService = LoginService(),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.service = service

    # -------------------------------------------------------
    #                     LISTAR (GET)
    # -------------------------------------------------------
    def list(self, request, *args, **kwargs):
        """Retorna todos los logins registrados."""
        logins = self.service.listar_logins()
        serializer = LoginDetailSerializer(logins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                 OBTENER (GET/{id})
    # -------------------------------------------------------
    def retrieve(self, request, *args, **kwargs):
        """Retorna un login por ID."""
        pk = kwargs.get("pk")
        login = self.service.obtener_login(id_login=pk)

        if not login:
            return Response(
                {"detail": "Login no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LoginDetailSerializer(login)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------------------------------------
    #                 CREAR (POST)
    # -------------------------------------------------------
    def create(self, request, *args, **kwargs):
        """
        Crea un nuevo registro de credenciales.
        Internamente el service aplica hashing con set_password()
        antes de guardar.
        """
        data = request.data.copy()

        try:
            login = self.service.crear_login(data)
            serializer = LoginDetailSerializer(login)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #               ACTUALIZAR (PUT/PATCH)
    # -------------------------------------------------------
    def update(self, request, *args, **kwargs):
        """Actualiza un registro de login existente."""
        pk = kwargs.get("pk")
        data = request.data.copy()

        try:
            login = self.service.actualizar_login(id_login=pk, data=data)
            serializer = LoginDetailSerializer(login)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #                 ELIMINAR (DELETE)
    # -------------------------------------------------------
    def destroy(self, request, *args, **kwargs):
        """Elimina un login."""
        pk = kwargs.get("pk")

        try:
            self.service.eliminar_login(id_login=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------
    #                LOGIN (POST /login)
    # -------------------------------------------------------
    @action(detail=False, methods=["post"], url_path="login")
    def autenticar(self, request):
        """
        Endpoint profesional para autenticación.
        Retorna:
            - usuario
            - token JWT (access)

        ejemplo: /api/auth/login/
        """
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            result = self.service.autenticar_usuario(username=username, password=password)
        except AuthenticationFailed as e:
            raise AuthenticationFailed(str(e))

        usuario_serializado = UsuarioSerializer(result["usuario"]).data
        response_data = {"usuario": usuario_serializado, "token": result["access"]}
        return Response(
        LoginResponseSerializer(response_data).data,
        status=status.HTTP_200_OK
        )
