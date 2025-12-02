from django.core.exceptions import ObjectDoesNotExist
from conductores.models.conductor import Conductor


class ConductorRepository:
    """
    Repositorio para el modelo Conductor.
    Encapsula todas las operaciones CRUD sobre la base de datos.
    """

    @staticmethod
    def get_all():
        """Retorna todos los conductores."""
        return Conductor.objects.all()

    @staticmethod
    def get_by_id(**kwargs):
        """
        Busca un conductor por cualquier campo.
        Ejemplo: get_by_id(id_conductor=1)
        Retorna None si no existe.
        """
        try:
            return Conductor.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_by_usuario(id_usuario):
        """
        Obtiene todos los conductores asociados a un usuario específico.
        Ejemplo: get_by_usuario(5)
        """
        return Conductor.objects.filter(usuario_id=id_usuario)

    @staticmethod
    def create(**kwargs):
        """
        Crea un nuevo conductor en la base de datos.
        Ejemplo:
        create(
            usuario=usuario_obj,
            licencia='ABC123',
            fecha_vencimiento='2025-06-10',
            licencia_vencida=False
        )
        """
        conductor = Conductor.objects.create(**kwargs)
        return conductor

    @staticmethod
    def update(id_conductor, **kwargs):
        """
        Actualiza un conductor por su ID.
        Ejemplo: update(1, licencia='XYZ999')
        Retorna el conductor actualizado o None si no existe.
        """
        conductor = ConductorRepository.get_by_id(id_conductor=id_conductor)
        if not conductor:
            return None

        for key, value in kwargs.items():
            setattr(conductor, key, value)
        conductor.save()
        return conductor

    @staticmethod
    def delete(id_conductor):
        """
        Elimina un conductor por su ID.
        Ejemplo: delete(1)
        Retorna True si se eliminó correctamente, False si no existe.
        """
        conductor = ConductorRepository.get_by_id(id_conductor=id_conductor)
        if not conductor:
            return False

        conductor.delete()
        return True