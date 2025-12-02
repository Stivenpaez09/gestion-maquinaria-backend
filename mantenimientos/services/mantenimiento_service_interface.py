from abc import ABC, abstractmethod


class IMantenimientoService(ABC):
    """
    Interfaz para el servicio de Mantenimientos.
    Define los métodos que cualquier implementación debe tener.
    """

    @abstractmethod
    def crear_mantenimiento(self, data: dict):
        pass

    @abstractmethod
    def listar_mantenimientos(self):
        pass

    @abstractmethod
    def obtener_mantenimiento(self, **kwargs):
        pass

    @abstractmethod
    def obtener_mantenimientos_por_maquina(self, id_maquina: int):
        pass

    @abstractmethod
    def obtener_mantenimientos_por_usuario(self, id_usuario: int):
        pass

    @abstractmethod
    def actualizar_mantenimiento(self, id_mantenimiento: int, data: dict):
        pass

    @abstractmethod
    def eliminar_mantenimiento(self, id_mantenimiento: int):
        pass

    @abstractmethod
    def obtener_ultimo_mantenimiento_por_maquina(self, id_maquina: int):
        pass

    @abstractmethod
    def obtener_ultimo_mantenimiento_por_maquina_y_tipo(self, id_maquina: int, tipo: str):
        pass