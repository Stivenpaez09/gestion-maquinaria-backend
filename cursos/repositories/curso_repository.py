from django.core.exceptions import ObjectDoesNotExist
from cursos.models.curso import Curso


class CursoRepository:
    """
    Repositorio para el modelo Curso.
    Encapsula todas las operaciones CRUD sobre la base de datos.
    """

    @staticmethod
    def get_all():
        """Retorna todos los cursos."""
        return Curso.objects.all()

    @staticmethod
    def get_by_id(**kwargs):
        """
        Busca un curso por cualquier campo.
        Ejemplo: get_by_id(id_curso=1)
        Retorna None si no existe.
        """
        try:
            return Curso.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_by_usuario(id_usuario):
        """
        Obtiene todos los cursos asociados a un usuario específico.
        Ejemplo: get_by_usuario(5)
        """
        return Curso.objects.filter(usuario_id=id_usuario)

    @staticmethod
    def create(**kwargs):
        """
        Crea un nuevo curso en la base de datos.
        Ejemplo:
        create(
            usuario=usuario_obj,
            nombre_curso='Python Avanzado',
            institucion='Universidad Nacional',
            fecha_inicio='2024-01-10',
            fecha_fin='2024-03-10'
        )
        """
        curso = Curso.objects.create(**kwargs)
        return curso

    @staticmethod
    def update(id_curso, **kwargs):
        """
        Actualiza un curso por su ID.
        Ejemplo: update(1, nombre_curso='Nuevo Nombre')
        Retorna el curso actualizado o None si no existe.
        """
        curso = CursoRepository.get_by_id(id_curso=id_curso)
        if not curso:
            return None

        for key, value in kwargs.items():
            setattr(curso, key, value)
        curso.save()
        return curso

    @staticmethod
    def delete(id_curso):
        """
        Elimina un curso por su ID.
        Ejemplo: delete(1)
        Retorna True si se eliminó correctamente, False si no existe.
        """
        curso = CursoRepository.get_by_id(id_curso=id_curso)
        if not curso:
            return False

        curso.delete()
        return True