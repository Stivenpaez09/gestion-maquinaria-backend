from django.core.exceptions import ObjectDoesNotExist
from usuarios.models.usuario import Usuario

class UsuarioRepository:
    """
        Repositorio para el modelo Usuario.
        Encapsula todas las operaciones CRUD sobre la base de datos.
        """

    @staticmethod
    def get_all():
        """Retorna todos los usuarios."""
        return Usuario.objects.all()

    @staticmethod
    def get_by_id(**kwargs):
        """
        Busca un usuario por cualquier campo.
        Ejemplo: get_by_id(id_usuario=1)
        Retorna None si no existe.
        """
        try:
            return Usuario.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_by_email(**kwargs):
        """
        Busca un usuario por cualquier campo (usualmente email).
        Ejemplo: get_by_email(email='correo@dominio.com')
        Retorna None si no existe.
        """
        try:
            return Usuario.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create(**kwargs):
        """Crea un usuario usando los campos enviados como kwargs."""
        usuario = Usuario.objects.create(**kwargs)
        return usuario

    @staticmethod
    def update(usuario: Usuario, **kwargs):
        """
        Actualiza un usuario existente.
        Recibe una instancia de Usuario y los campos a actualizar como kwargs.
        """
        for key, value in kwargs.items():
            setattr(usuario, key, value)
        usuario.save()
        return usuario

    @staticmethod
    def delete(usuario: Usuario):
        """Elimina el usuario enviado."""
        usuario.delete()
        return True