from abc import ABC, abstractmethod
from decimal import Decimal

from proyecto_maquinaria.models.proyecto_maquinaria import ProyectoMaquinaria


class IProyectoMaquinariaService(ABC):
    """
    Interface profesional para la gestión de ProyectoMaquinaria.
    Define los métodos que deben implementarse en el service.
    """

    @abstractmethod
    def listar_asignaciones(self):
        pass

    @abstractmethod
    def obtener_asignacion(self, id_proyecto_maquinaria: int):
        pass

    @abstractmethod
    def crear_asignacion(self, data: dict):
        pass

    @abstractmethod
    def actualizar_asignacion(self, id_proyecto_maquinaria: int, data: dict):
        pass

    @abstractmethod
    def eliminar_asignacion(self, id_proyecto_maquinaria: int):
        pass

    @abstractmethod
    def sumar_horas_acumuladas(self, proyecto_maquinaria: ProyectoMaquinaria, horas_a_sumar: Decimal):
        pass

    @abstractmethod
    def obtener_ultimo_proyecto_por_maquina(self, id_maquina: int):
        pass
