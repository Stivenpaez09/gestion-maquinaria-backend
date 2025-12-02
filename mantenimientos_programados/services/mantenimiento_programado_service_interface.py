from abc import ABC, abstractmethod


class IMantenimientoProgramadoService(ABC):
    """
    Interface para el servicio de Mantenimiento Programado.
    Define los métodos obligatorios siguiendo principios SOLID.
    """

    @abstractmethod
    def crear_mantenimiento_programado(self, data: dict):
        """Crea un nuevo mantenimiento programado."""
        pass

    @abstractmethod
    def listar_mantenimientos_programados(self):
        """Retorna todos los mantenimientos programados."""
        pass

    @abstractmethod
    def obtener_mantenimiento_programado(self, **kwargs):
        """
        Obtiene un mantenimiento programado por cualquier campo.
        Ejemplo: obtener_mantenimiento_programado(id_programado=1)
        """
        pass

    @abstractmethod
    def obtener_mantenimientos_por_maquina(self, id_maquina: int):
        """
        Obtiene todos los mantenimientos programados asociados a una máquina.
        """
        pass

    @abstractmethod
    def actualizar_mantenimiento_programado(self, id_programado: int, data: dict):
        """Actualiza un mantenimiento programado."""
        pass

    @abstractmethod
    def eliminar_mantenimiento_programado(self, id_programado: int):
        """Elimina un mantenimiento programado."""
        pass

    @abstractmethod
    def obtener_mantenimiento_programado_por_maquina_y_tipo(self, id_maquina: int, tipo: str):
        """
        Obtiene un mantenimiento programado por máquina y tipo.
        Ejemplo: obtener_mantenimiento_programado_por_maquina_y_tipo(3, 'Cambio de aceite')
        """
        pass