from django.core.exceptions import ObjectDoesNotExist
from hojas_vida.models.hoja_vida import HojaVida


class HojaVidaRepository:
    """
    Repositorio para el modelo HojaVida.
    Encapsula todas las operaciones CRUD sobre la base de datos.
    """

    @staticmethod
    def get_all():
        """Retorna todas las hojas de vida."""
        return HojaVida.objects.all()

    @staticmethod
    def get_by_id(**kwargs):
        """
        Busca una hoja de vida por cualquier campo.
        Ejemplo: get_by_id(id_hoja=1)
        Retorna None si no existe.
        """
        try:
            return HojaVida.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_by_maquinaria(**kwargs):
        """
        Busca hojas de vida asociadas a una maquinaria específica.
        Ejemplo: get_by_maquinaria(maquinaria_id=1)
        Retorna queryset vacío si no existen registros.
        """
        return HojaVida.objects.filter(**kwargs)

    @staticmethod
    def create(**kwargs):
        """
        Crea una hoja de vida usando los campos enviados como kwargs.
        Ejemplo: create(maquinaria=maquina, usuario=usuario, descripcion="...")
        """
        hoja = HojaVida.objects.create(**kwargs)
        return hoja

    @staticmethod
    def update(hoja: HojaVida, **kwargs):
        """
        Actualiza una hoja de vida existente.
        Recibe una instancia de HojaVida y los campos a actualizar como kwargs.
        """
        for key, value in kwargs.items():
            setattr(hoja, key, value)
        hoja.save()
        return hoja

    @staticmethod
    def delete(hoja: HojaVida):
        """Elimina la hoja de vida enviada."""
        hoja.delete()
        return True