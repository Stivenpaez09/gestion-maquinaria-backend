from abc import ABC, abstractmethod


class IRegistroHorasMaquinariaService(ABC):
    """
    Interfaz para el servicio de Registro de Horas de Maquinaria.
    Define las operaciones principales para manejar:
    - CRUD de registros de horas
    - Reglas de negocio asociadas a horas acumuladas
    """

    @abstractmethod
    def listar_registros(self):
        """Retorna todos los registros de horas."""
        pass

    @abstractmethod
    def obtener_registro(self, id_registro: int):
        """Obtiene un registro por ID. Lanza NotFound si no existe."""
        pass

    @abstractmethod
    def crear_registro(self, data: dict):
        """Crea un registro de horas con validación y actualiza acumulados."""
        pass

    @abstractmethod
    def actualizar_registro(self, id_registro: int, data: dict):
        """Actualiza parcialmente un registro existente."""
        pass

    @abstractmethod
    def eliminar_registro(self, id_registro: int):
        """Elimina un registro por ID."""
        pass

    # --------------------------------------------------------------
    # Filtros
    # --------------------------------------------------------------
    @abstractmethod
    def obtener_por_maquina(self, id_maquina: int):
        """Retorna registros filtrados por máquina."""
        pass

    @abstractmethod
    def obtener_por_proyecto(self, id_proyecto: int):
        """Retorna registros filtrados por proyecto."""
        pass

    @abstractmethod
    def obtener_por_fecha(self, fecha):
        """Retorna registros realizados en la fecha dada."""
        pass

    @abstractmethod
    def obtener_entre_fechas(self, fecha_inicio, fecha_fin):
        """Retorna registros entre dos fechas."""
        pass
