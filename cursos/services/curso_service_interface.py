from abc import ABC, abstractmethod


class ICursoService(ABC):
    """
        Interfaz para el servicio de Cursos.
        Define las operaciones necesarias para la gestión de cursos.
    """

    @abstractmethod
    def crear_curso(self, data: dict):
        pass

    @abstractmethod
    def listar_cursos(self):
        pass

    @abstractmethod
    def obtener_curso(self, **kwargs):
        pass

    @abstractmethod
    def obtener_cursos_por_usuario(self, id_usuario: int):
        pass

    @abstractmethod
    def actualizar_curso(self, id_curso: int, data: dict):
        pass

    @abstractmethod
    def eliminar_curso(self, id_curso: int):
        pass
