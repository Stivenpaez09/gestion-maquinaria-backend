from django.core.exceptions import ObjectDoesNotExist

from logins.models.login import Login


class LoginRepository:
    """
    Repositorio para el modelo Login.
    Encapsula todas las operaciones CRUD y las consultas
    específicas relacionadas con credenciales y autenticación.
    """

    # -------------------------
    # Consultas generales
    # -------------------------

    @staticmethod
    def get_all():
        """Retorna todos los logins registrados."""
        return Login.objects.all()

    @staticmethod
    def get_by_id(**kwargs):
        """
        Busca un login por cualquier campo.
        Ejemplo: get_by_id(id_login=1)
        Retorna None si no existe.
        """
        try:
            return Login.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_by_username(username: str):
        """
        Busca un login usando el username.
        Retorna None si no existe.
        """
        try:
            return Login.objects.get(username=username)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_active():
        """Retorna todos los logins que están activos."""
        return Login.objects.filter(is_active=True)

    @staticmethod
    def get_by_usuario(usuario_id: int):
        """
        Busca un login relacionado con un usuario específico.
        Retorna None si no existe.
        """
        try:
            return Login.objects.get(usuario__id_usuario=usuario_id)
        except ObjectDoesNotExist:
            return None

    # -------------------------
    # Operaciones CRUD
    # -------------------------
    @staticmethod
    def create(login_instance: Login) -> Login:
        """
        Guarda una instancia existente de Login.
        """
        login_instance.save()
        return login_instance

    @staticmethod
    def update(login: Login, **kwargs):
        """
        Actualiza un login existente.
        Recibe una instancia de Login y los campos a actualizar como kwargs.
        OJO: si se envía 'password', debe ser encriptada en el Service.
        """
        for key, value in kwargs.items():
            setattr(login, key, value)
        login.save()
        return login

    @staticmethod
    def delete(login: Login):
        """
        Elimina un login existente.
        """
        login.delete()
        return True