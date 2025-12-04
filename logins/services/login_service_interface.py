from abc import ABC, abstractmethod


class ILoginService(ABC):
    """
    Interfaz profesional para el servicio de Login.
    Define las operaciones que cualquier implementación debe cumplir.
    """

    @abstractmethod
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
        pass

    @abstractmethod
    def autenticar_usuario(self, username: str, password: str):
        """
        Autentica un usuario con email y contraseña.
        Retorna un diccionario con:
        - usuario: instancia del usuario autenticado
        - token: token generado

        Lanza AuthenticationFailed si las credenciales son inválidas.
        """
        pass

    @abstractmethod
    def listar_logins(self):
        """
        Retorna todos los logins registrados.
        """
        pass

    @abstractmethod
    def obtener_login(self, id_login: int):
        """
        Retorna el login con el ID registrado.
        """
        pass

    @abstractmethod
    def obtener_login_por_usuario(self, usuario_id: int):
        """
        Retorna el login con el usuario registrado.
        """
        pass

    @abstractmethod
    def actualizar_login(self, id_login: int, data: dict):
        """
        Actualiza credenciales.
        Si viene password → se encripta ANTES de guardar.
        """
        pass

    @abstractmethod
    def eliminar_login(self, id_login: int):
        """
        Eliminar el login con el ID registrado.
        """
        pass