from abc import ABC, abstractmethod


class IConductorService(ABC):
    """
    Interfaz para el servicio de Conductores.
    Define los métodos que cualquier implementación debe tener.
    """

    @abstractmethod
    def crear_conductor(self, data: dict):
        pass

    @abstractmethod
    def listar_conductores(self):
        pass

    @abstractmethod
    def obtener_conductor(self, **kwargs):
        pass

    @abstractmethod
    def actualizar_conductor(self, id_conductor: int, data: dict):
        pass

    @abstractmethod
    def eliminar_conductor(self, id_conductor: int):
        pass
