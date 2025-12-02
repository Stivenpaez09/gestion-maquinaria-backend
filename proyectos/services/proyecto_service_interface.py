from abc import ABC, abstractmethod


class IProyectoService(ABC):
    """Interfaz para el servicio de Proyectos."""

    @abstractmethod
    def crear_proyecto(self, data: dict):
        pass

    @abstractmethod
    def listar_proyectos(self):
        pass

    @abstractmethod
    def obtener_proyecto(self, **kwargs):
        pass

    @abstractmethod
    def actualizar_proyecto(self, id_proyecto: int, data: dict):
        pass

    @abstractmethod
    def eliminar_proyecto(self, id_proyecto: int):
        pass

    @abstractmethod
    def listar_proyectos_por_empresa(self, id_empresa: int):
        pass