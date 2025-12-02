from django.core.exceptions import ObjectDoesNotExist

from mantenimientos_programados.models.mantenimiento_programado import MantenimientoProgramado


class MantenimientoProgramadoRepository:
    """
    Repositorio para el modelo MantenimientoProgramado.
    Encapsula todas las operaciones CRUD sobre la base de datos.
    """


    @staticmethod
    def get_all():
        """Retorna todos los mantenimientos programados."""
        return MantenimientoProgramado.objects.all()

    @staticmethod
    def get_by_id(**kwargs):
        """
        Busca un mantenimiento programado por cualquier campo.
        Ejemplo:
            get_by_id(id_programado=1)

        Retorna None si no existe.
        """
        try:
            return MantenimientoProgramado.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_by_maquina(id_maquina: int):
        """
        Obtiene todos los mantenimientos programados asociados a una máquina específica.
        Ejemplo:
            get_by_maquina(3)
        """
        return MantenimientoProgramado.objects.filter(maquina_id=id_maquina)

    @staticmethod
    def get_by_maquina_y_tipo(id_maquina: int, tipo: str):
        """
        Obtiene un mantenimiento programado por máquina y tipo.
        
        Ejemplo:
            get_by_maquina_y_tipo(5, 'preventivo')
        
        Retorna None si no existe.
        """
        try:
            return MantenimientoProgramado.objects.get(
                maquina_id=id_maquina,
                tipo=tipo
            )
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create(**kwargs):
        """
        Crea un nuevo mantenimiento programado.
        Ejemplo:
            create(
                maquina=maquina_obj,
                tipo="Cambio de aceite",
                intervalo_horas=200,
                descripcion="Cambio de aceite cada 200 horas."
            )
        """
        mantenimiento = MantenimientoProgramado.objects.create(**kwargs)
        return mantenimiento

    @staticmethod
    def update(id_programado: int, **kwargs):
        """
        Actualiza un mantenimiento programado por su ID.
        Ejemplo:
            update(1, tipo="Nuevo tipo")

        Retorna el objeto actualizado o None si no existe.
        """
        mantenimiento = MantenimientoProgramadoRepository.get_by_id(id_programado=id_programado)

        if not mantenimiento:
            return None

        for key, value in kwargs.items():
            setattr(mantenimiento, key, value)

        mantenimiento.save()
        return mantenimiento

    @staticmethod
    def delete(id_programado: int):
        """
        Elimina un mantenimiento programado por su ID.
        Ejemplo:
            delete(1)

        Retorna True si se eliminó correctamente, False si no existe.
        """
        mantenimiento = MantenimientoProgramadoRepository.get_by_id(id_programado=id_programado)

        if not mantenimiento:
            return False

        mantenimiento.delete()
        return True