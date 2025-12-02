from django.core.exceptions import ObjectDoesNotExist

from registros_horas_maquinaria.models.registro_horas_maquinaria import RegistroHorasMaquinaria


class RegistroHorasMaquinariaRepository:
    """
    Repositorio para el modelo RegistroHorasMaquinaria.
    Encapsula todas las operaciones CRUD y consultas
    personalizadas sobre la base de datos.
    """

    # ---------------------------------------------------------
    # CRUD BÁSICO
    # ---------------------------------------------------------

    @staticmethod
    def get_all():
        """Retorna todos los registros de horas."""
        return RegistroHorasMaquinaria.objects.all()

    @staticmethod
    def get_by_id(**kwargs):
        """
        Busca un registro por cualquier campo.
        Ejemplo: get_by_id(id_registro=1)
        Retorna None si no existe.
        """
        try:
            return RegistroHorasMaquinaria.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create(**kwargs):
        """
        Crea un nuevo registro de horas.
        Ejemplo:
        create(
            maquina=maquina_obj,
            proyecto=proyecto_obj,
            fecha='2024-06-11',
            horas_trabajadas=5.5,
            observaciones='Turno extra'
        )
        """
        return RegistroHorasMaquinaria.objects.create(**kwargs)

    @staticmethod
    def update(id_registro, **kwargs):
        """
        Actualiza un registro de horas por su ID.
        Ejemplo:
        update(3, horas_trabajadas=7.5)

        Retorna el registro actualizado o None si no existe.
        """
        registro = RegistroHorasMaquinariaRepository.get_by_id(id_registro=id_registro)
        if not registro:
            return None

        for key, value in kwargs.items():
            setattr(registro, key, value)

        registro.save()
        return registro

    @staticmethod
    def delete(id_registro):
        """
        Elimina un registro por su ID.
        Ejemplo: delete(2)
        Retorna True si se eliminó, False si no existe.
        """
        registro = RegistroHorasMaquinariaRepository.get_by_id(id_registro=id_registro)
        if not registro:
            return False

        registro.delete()
        return True

    # ---------------------------------------------------------
    # CONSULTAS PERSONALIZADAS
    # ---------------------------------------------------------

    @staticmethod
    def get_by_maquina(id_maquina):
        """
        Obtiene todos los registros de horas asociados a una máquina.
        Ejemplo: get_by_maquina(4)
        """
        return RegistroHorasMaquinaria.objects.filter(maquina_id=id_maquina)

    @staticmethod
    def get_by_proyecto(id_proyecto):
        """
        Obtiene todos los registros de horas pertenecientes a un proyecto.
        Ejemplo: get_by_proyecto(10)
        """
        return RegistroHorasMaquinaria.objects.filter(proyecto_id=id_proyecto)

    @staticmethod
    def get_by_fecha(fecha):
        """
        Obtiene los registros realizados en una fecha específica.
        Ejemplo: get_by_fecha('2024-01-05')
        """
        return RegistroHorasMaquinaria.objects.filter(fecha=fecha)

    @staticmethod
    def get_between_fechas(fecha_inicio, fecha_fin):
        """
        Obtiene registros de horas entre dos fechas.
        Ejemplo:
        get_between_fechas('2024-01-01', '2024-01-31')
        """
        return RegistroHorasMaquinaria.objects.filter(
            fecha__range=(fecha_inicio, fecha_fin)
        )

    @staticmethod
    def search_observaciones(texto):
        """
        Busca registros por coincidencias en observaciones.
        Ejemplo: search_observaciones('falla', 'aceite')
        """
        return RegistroHorasMaquinaria.objects.filter(
            observaciones__icontains=texto
        )

    @staticmethod
    def get_total_horas_by_maquina(id_maquina):
        """
        Retorna la suma total de horas registradas para una máquina.
        Ideal para reportes.
        """
        from django.db.models import Sum
        return (
            RegistroHorasMaquinaria.objects
            .filter(maquina_id=id_maquina)
            .aggregate(total=Sum('hojas_trabajadas'))
        )

    @staticmethod
    def get_total_horas_by_proyecto(id_proyecto):
        """
        Retorna la suma total de horas registradas para un proyecto.
        """
        from django.db.models import Sum
        return (
            RegistroHorasMaquinaria.objects
            .filter(proyecto_id=id_proyecto)
            .aggregate(total=Sum('horas_trabajadas'))
        )