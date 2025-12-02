from abc import ABC, abstractmethod
from decimal import Decimal

from maquinarias.models.maquinaria import Maquinaria


class IMaquinariaService(ABC):
    """
    Interfaz para el servicio de Maquinaria.
    Define las operaciones permitidas.
    """

    @abstractmethod
    def crear_maquinaria(self, data: dict):
        pass

    @abstractmethod
    def listar_maquinarias(self):
        pass

    @abstractmethod
    def obtener_maquinaria(self, **kwargs):
        pass

    @abstractmethod
    def actualizar_maquinaria(self, id_maquina: int, data: dict):
        pass

    @abstractmethod
    def sumar_horas_maquinaria(self, maquina: Maquinaria, horas_a_sumar: Decimal):
        pass

    @abstractmethod
    def actualizar_estado_maquinaria(self, id_maquina: int, estado: str):
        pass

    @abstractmethod
    def eliminar_maquinaria(self, id_maquina: int):
        pass

    @abstractmethod
    def obtener_resumen_maquinarias(self):
        pass
