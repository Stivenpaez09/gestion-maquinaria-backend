from decimal import Decimal, InvalidOperation

from django.core.exceptions import ObjectDoesNotExist

from maquinarias.models.maquinaria import Maquinaria

class MaquinariaRepository:
    """
    Repositorio para el modelo Maquinaria.
    Encapsula todas las operaciones CRUD sobre la base de datos.
    """

    @staticmethod
    def get_all():
        """Retorna todas las maquinarias."""
        return Maquinaria.objects.all()

    @staticmethod
    def get_by(**kwargs):
        """
        Busca una maquinaria por cualquier campo.
        Ejemplo: get_by_id(id_maquina=1)
        Retorna None si no existe.
        """
        try:
            return Maquinaria.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None


    @staticmethod
    def filter_by_estado(estado):
        """
        Retorna todas las maquinarias con un estado específico.
        Ejemplo: filter_by_estado('operativa')
        """
        return Maquinaria.objects.filter(estado=estado)

    @staticmethod
    def create(**kwargs):
        """
        Crea una nueva maquinaria en la base de datos.
        Ejemplo:
        create(
            nombre_maquina='Excavadora',
            modelo='CAT320',
            marca='Caterpillar',
            serie='XH23LL99',
            fecha_adquisicion='2024-10-10',
            horas_totales=120.5,
            estado='operativa'
        )
        """
        maquinaria = Maquinaria.objects.create(**kwargs)
        return maquinaria

    @staticmethod
    def update(maquinaria, **kwargs):
        """
        Actualiza una maquinaria por su ID.
        Ejemplo: update(1, nombre_maquina='Taladro Nuevo')
        Retorna la maquinaria actualizada o None si no existe.
        """

        for key, value in kwargs.items():
            setattr(maquinaria, key, value)
        maquinaria.save()
        return maquinaria

    @staticmethod
    def update_horas_totales(maquina: Maquinaria, horas_a_sumar):
        """
        Actualiza las horas totales de una maquinaria sumando un valor dado.

        Parámetros:
        - maquina: instancia de Maquinaria (no un ID).
        - horas_a_sumar: cantidad de horas a añadir (puede ser decimal).

        Retorna:
        - maquinaria actualizada.
        - None si la instancia no es válida.
        """
        if not maquina or not isinstance(maquina, Maquinaria):
            return None

        maquina.horas_totales = maquina.horas_totales + horas_a_sumar
        maquina.save()
        return maquina

    @staticmethod
    def update_estado(maquinaria: Maquinaria):
        """
            Actualiza el estado de una maquinaria guardando la instancia.

            Parámetros:
            - maquinaria: instancia de Maquinaria con el estado ya modificado.

            Retorna:
            - La maquinaria actualizada.
            - None si la instancia no es válida.
            """
        if not maquinaria or not isinstance(maquinaria, Maquinaria):
            return None
        maquinaria.save()
        return maquinaria

    @staticmethod
    def delete(id_maquina):
        """
        Elimina una maquinaria por su ID.
        Ejemplo: delete(1)
        Retorna True si se eliminó correctamente, False si no existe.
        """
        maquinaria = MaquinariaRepository.get_by(id_maquina=id_maquina)
        if not maquinaria:
            return False
        maquinaria.delete()
        return True