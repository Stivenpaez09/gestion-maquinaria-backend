from django.core.exceptions import ObjectDoesNotExist
from proyectos.models.proyecto import Proyecto


class ProyectoRepository:
    """
    Repositorio para el modelo Proyecto.
    Encapsula todas las operaciones CRUD sobre la base de datos.
    """

    @staticmethod
    def get_all():
        """Retorna todos los proyectos."""
        return Proyecto.objects.all()

    @staticmethod
    def get_by_id(**kwargs):
        """
        Busca un proyecto por cualquier campo.
        Ejemplo: get_by_id(id_proyecto=1)
        Retorna None si no existe.
        """
        try:
            return Proyecto.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def filter_by_fecha_inicio(fecha_inicio):
        """
        Retorna todos los proyectos que tengan la fecha de inicio especificada.
        Ejemplo: filter_by_fecha_inicio('2025-01-01')
        """
        return Proyecto.objects.filter(fecha_inicio=fecha_inicio)

    @staticmethod
    def create(**kwargs):
        """
        Crea un nuevo proyecto en la base de datos.
        Ejemplo: create(
            nombre_proyecto='Proyecto X',
            descripcion='Descripción del proyecto',
            fecha_inicio='2025-01-01',
            fecha_fin='2025-06-01'
        )
        """
        proyecto = Proyecto.objects.create(**kwargs)
        return proyecto

    @staticmethod
    def update(id_proyecto, **kwargs):
        """
        Actualiza un proyecto por su ID.
        Ejemplo: update(1, nombre_proyecto='Proyecto Modificado')
        Retorna el proyecto actualizado o None si no existe.
        """
        proyecto = ProyectoRepository.get_by_id(id_proyecto=id_proyecto)
        if not proyecto:
            return None

        for key, value in kwargs.items():
            setattr(proyecto, key, value)
        proyecto.save()
        return proyecto

    @staticmethod
    def delete(id_proyecto):
        """
        Elimina un proyecto por su ID.
        Ejemplo: delete(1)
        Retorna True si se eliminó correctamente, False si no existe.
        """
        proyecto = ProyectoRepository.get_by_id(id_proyecto=id_proyecto)
        if not proyecto:
            return False
        proyecto.delete()
        return True

    @staticmethod
    def get_by_empresa(id_empresa):
        """
        Retorna todos los proyectos asociados a una empresa específica.

        Ejemplo:
            get_by_empresa(5)  -> proyectos donde empresa_id = 5
        """
        return Proyecto.objects.filter(empresa_id=id_empresa)