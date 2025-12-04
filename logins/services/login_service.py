import time

from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from logins.models.login import Login
from logins.repositories.login_repository import LoginRepository
from logins.serializers.login_create_serializer import LoginCreateSerializer
from logins.services.login_service_interface import ILoginService


class LoginService(ILoginService):
    """
    Servicio profesional para la autenticación de logins.
    """

    # ================================================================
    # Crear Login
    # ================================================================
    def crear_login(self, data: dict):
        """
        Crea un registro de Login (credenciales).
        Pasos:
        1. Validar datos con serializer.
        2. Verificar username único.
        3. Crear el objeto (sin hash).
        4. Aplicar set_password() para hashear.
        5. Guardar credenciales.
        """

        data = data.copy()
        serializer = LoginCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        raw_password = serializer.validated_data["password"]

        # 1. Regla de negocio → username único
        if LoginRepository.get_by_username(username=username):
            raise ValidationError({"username": "Este nombre de usuario ya existe."})

        login = Login(
            usuario=serializer.validated_data.get("usuario"),
            username=username,
            rol=serializer.validated_data.get("rol", "OPERADOR")
        )

        # 3. Aplicar hashing ANTES de guardar
        login.set_password(raw_password)

        # 4. Persistir usando el repository
        login = LoginRepository.create(login)

        return login

    # ================================================================
    # Autenticar y retornar token
    # ================================================================
    def autenticar_usuario(self, username: str, password: str):
        """
        Autentica un usuario con email y contraseña.
        Retorna un diccionario con:
        - usuario: instancia del usuario autenticado
        - token: token generado

        Lanza AuthenticationFailed si las credenciales son inválidas.
        """

        # 1. Buscar credenciales
        login = LoginRepository.get_by_username(username=username)
        if not login or not login.is_active:
            raise AuthenticationFailed("Credenciales inválidas.")

        # 2. Validar contraseña
        if not login.check_password(password):
            raise AuthenticationFailed("Credenciales inválidas.")

        # 3. Usuario asociado
        usuario = login.usuario

        # 4. Generar JWT con claims personalizados
        refresh = RefreshToken.for_user(login)
        access = refresh.access_token
        # Campos extra en el token
        access["rol"] = login.rol
        access["username"] = login.username
        access["iat"] = int(time.time())

        return {
            "usuario": usuario,
            "access": str(access),
        }

    # ================================================================
    # LISTAR LOGINS
    # ================================================================
    def listar_logins(self):
        """
        Retorna todos los logins registrados.
        """
        return LoginRepository.get_all()

    # ================================================================
    # OBTENER LOGIN POR ID
    # ================================================================
    def obtener_login(self, id_login: int):
        login = LoginRepository.get_by_id(id_login=id_login)
        if not login:
            raise ValidationError({"detail": "Login no encontrado."})
        return login

    # ================================================================
    # OBTENER LOGIN POR USUARIO
    # ================================================================
    def obtener_login_por_usuario(self, usuario_id: int):
        login = LoginRepository.get_by_usuario(usuario_id)
        if not login:
            raise ValidationError({"detail": "El usuario no tiene login asociado."})
        return login

    # ================================================================
    # ACTUALIZAR LOGIN
    # ================================================================
    def actualizar_login(self, id_login: int, data: dict):
        """
        Actualiza credenciales.
        Si viene password → se encripta ANTES de guardar.
        """

        login = LoginRepository.get_by_id(id_login=id_login)
        if not login:
            raise ValidationError({"detail": "Login no encontrado."})

        serializer = LoginCreateSerializer(data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data

        # Si se envía password, debe hashearse
        if "password" in validated:
            raw_password = validated.pop("password")
            login.set_password(raw_password)

        if "username" in validated:
            existing = LoginRepository.get_by_username(validated["username"])

            if existing and existing.id_login != login.id_login:
                raise ValidationError({"username": "Este nombre de usuario ya existe."})


        # Actualizar con el repository
        login = LoginRepository.update(login, **validated)

        return login

    # ================================================================
    # ELIMINAR LOGIN
    # ================================================================
    def eliminar_login(self, id_login: int):
        login = LoginRepository.get_by_id(id_login=id_login)
        if not login:
            raise ValidationError({"detail": "Login no encontrado."})

        LoginRepository.delete(login)
        return True