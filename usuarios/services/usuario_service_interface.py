from abc import ABC, abstractmethod


class IUsuarioService(ABC):
    """
    Interfaz profesional para la gestión de usuarios.
    Define los métodos que todo servicio de usuarios debe implementar.
    """

    @abstractmethod
    def listar_usuarios(self):
        pass

    @abstractmethod
    def obtener_usuario(self, id_usuario: int):
        pass

    @abstractmethod
    def crear_usuario(self, data: dict):
        pass

    @abstractmethod
    def actualizar_usuario(self, id_usuario: int, data: dict):
        pass

    @abstractmethod
    def eliminar_usuario(self, id_usuario: int):
        pass