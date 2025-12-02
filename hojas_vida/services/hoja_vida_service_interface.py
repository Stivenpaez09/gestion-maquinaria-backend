from abc import ABC, abstractmethod


class IHojaVidaService(ABC):
    """
    Interfaz para el servicio de HojaVida.
    Define los métodos que deben implementarse en el servicio.
    """

    @abstractmethod
    def listar_hojas_vida(self):
        pass

    @abstractmethod
    def obtener_hoja_vida(self, id_hoja: int):
        pass

    @abstractmethod
    def crear_hoja_vida(self, data: dict):
        pass

    @abstractmethod
    def actualizar_hoja_vida(self, id_hoja: int, data: dict):
        pass

    @abstractmethod
    def eliminar_hoja_vida(self, id_hoja: int):
        pass
