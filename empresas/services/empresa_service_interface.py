from abc import ABC, abstractmethod

class IEmpresaService(ABC):
    """
    Interfaz del servicio de lógica de negocio para Empresas.
    Define los métodos obligatorios para cualquier implementación
    del servicio de empresas, siguiendo principios SOLID (ISP).
    """

    @abstractmethod
    def crear_empresa(self, data: dict):
        """Crear una nueva empresa."""
        pass

    @abstractmethod
    def listar_empresas(self):
        """Listar todas las empresas registradas."""
        pass

    @abstractmethod
    def obtener_empresa(self, **kwargs):
        """Obtener una empresa por ID u otro campo único."""
        pass

    @abstractmethod
    def actualizar_empresa(self, id_empresa: int, data: dict):
        """Actualizar una empresa (PUT o PATCH)."""
        pass

    @abstractmethod
    def eliminar_empresa(self, id_empresa: int):
        """Eliminar una empresa por su ID."""
        pass
