from django.core.exceptions import ObjectDoesNotExist

from empresas.models.empresa import Empresa


class EmpresaRepository:
    """
    Repositorio para el modelo Empresa.
    Encapsula todas las operaciones CRUD sobre la base de datos.
    """

    # ---------------------------------------------------------
    #                    LISTAR TODOS
    # ---------------------------------------------------------
    @staticmethod
    def get_all():
        """Retorna todas las empresas registradas."""
        return Empresa.objects.all()

    # ---------------------------------------------------------
    #                     OBTENER POR CAMPO
    # ---------------------------------------------------------
    @staticmethod
    def get_by_id(**kwargs):
        """
        Busca una empresa por cualquier campo.
        Ejemplo:
            get_by_id(id_empresa=1)
            get_by_id(nit="900123456")
        Retorna None si no existe.
        """
        try:
            return Empresa.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    # ---------------------------------------------------------
    #                       CREAR
    # ---------------------------------------------------------
    @staticmethod
    def create(**kwargs):
        """
        Crea una nueva empresa en la base de datos.
        Ejemplo:
        create(
            nombre="Tecnologías ABC",
            nit="901234567",
            telefono="3205558888",
            direccion="Calle 45 #12-33",
            email="contacto@abc.com"
        )
        """
        empresa = Empresa.objects.create(**kwargs)
        return empresa

    # ---------------------------------------------------------
    #                     ACTUALIZAR
    # ---------------------------------------------------------
    @staticmethod
    def update(id_empresa, **kwargs):
        """
        Actualiza una empresa por su ID.
        Ejemplo:
            update(1, nombre="Empresa Actualizada")
        Retorna la empresa actualizada o None si no existe.
        """
        empresa = EmpresaRepository.get_by_id(id_empresa=id_empresa)
        if not empresa:
            return None

        for key, value in kwargs.items():
            setattr(empresa, key, value)

        empresa.save()
        return empresa

    # ---------------------------------------------------------
    #                       ELIMINAR
    # ---------------------------------------------------------
    @staticmethod
    def delete(id_empresa):
        """
        Elimina una empresa por su ID.
        Ejemplo:
            delete(1)
        Retorna True si se eliminó correctamente, False si no existe.
        """
        empresa = EmpresaRepository.get_by_id(id_empresa=id_empresa)
        if not empresa:
            return False

        empresa.delete()
        return True