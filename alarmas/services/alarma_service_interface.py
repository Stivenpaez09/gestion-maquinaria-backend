from abc import ABC, abstractmethod


class IAlarmaService(ABC):
    """
    Interfaz que define los contratos del servicio de Alarmas.
    """

    @abstractmethod
    def validar_y_generar_alarmas(self, id_maquina: int):
        """
        Método principal: valida horas de mantenimiento y genera
        alarmas según corresponda (crítica o media).
        """
        pass

    @abstractmethod
    def listar_alarmas(self):
        """Lista todas las alarmas."""
        pass

    @abstractmethod
    def obtener_alarma(self, id_alarma: int):
        """Obtiene una alarma por ID."""
        pass

    @abstractmethod
    def marcar_como_vista(self, id_alarma: int):
        """Marca una alarma como vista."""
        pass

    @abstractmethod
    def eliminar_alarma(self, id_alarma: int):
        """Elimina una alarma."""
        pass

    @abstractmethod
    def obtener_alarmas_por_maquina(self, id_maquina: int):
        """Obtiene alarmas de una máquina específica."""
        pass

    @abstractmethod
    def obtener_alarmas_no_vistas(self):
        """Obtiene todas las alarmas sin ver."""
        pass

    @abstractmethod
    def obtener_cantidad_alarmas_no_vistas(self):
        """Obtiene la cantidad de alarmas sin ver."""
        pass

    @abstractmethod
    def obtener_estadisticas(self):
        """Retorna estadísticas del dashboard."""
        pass