from django.core.exceptions import ObjectDoesNotExist

from mantenimientos.models.mantenimiento import Mantenimiento


class MantenimientoRepository:
    """
    Repositorio para el modelo Mantenimiento.
    Encapsula todas las operaciones CRUD y consultas personalizadas
    sobre la base de datos.
    """

    @staticmethod
    def get_all():
        """Retorna todos los mantenimientos."""
        return Mantenimiento.objects.all()

    @staticmethod
    def get_by_id(**kwargs):
        """
        Busca un mantenimiento por cualquier campo.
        Ejemplo: get_by_id(id_mantenimiento=1)
        Retorna None si no existe.
        """
        try:
            return Mantenimiento.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create(**kwargs):
        """
        Crea un nuevo mantenimiento en la base de datos.
        Ejemplo:
        create(
            maquina=maquina_obj,
            usuario=usuario_obj,
            tipo_mantenimiento='preventivo',
            descripcion='Cambio de aceite',
            fecha_mantenimiento='2024-03-01',
            costo=150000
        )
        """
        mantenimiento = Mantenimiento.objects.create(**kwargs)
        return mantenimiento

    @staticmethod
    def update(id_mantenimiento, **kwargs):
        """
        Actualiza un mantenimiento por su ID.
        Ejemplo: update(1, descripcion='Nueva descripción')
        Retorna el mantenimiento actualizado o None si no existe.
        """
        mantenimiento = MantenimientoRepository.get_by_id(id_mantenimiento=id_mantenimiento)
        if not mantenimiento:
            return None

        for key, value in kwargs.items():
            setattr(mantenimiento, key, value)

        mantenimiento.save()
        return mantenimiento

    @staticmethod
    def delete(id_mantenimiento):
        """
        Elimina un mantenimiento por su ID.
        Ejemplo: delete(1)
        Retorna True si se eliminó correctamente, False si no existe.
        """
        mantenimiento = MantenimientoRepository.get_by_id(id_mantenimiento=id_mantenimiento)
        if not mantenimiento:
            return False

        mantenimiento.delete()
        return True


    @staticmethod
    def get_by_maquina(id_maquina):
        """
        Obtiene todos los mantenimientos asociados a una máquina.
        Ejemplo: get_by_maquina(3)
        """
        return Mantenimiento.objects.filter(maquina_id=id_maquina)

    @staticmethod
    def get_by_usuario(id_usuario):
        """
        Obtiene todos los mantenimientos realizados por un usuario.
        (Recordar que usuario puede ser NULL)
        Ejemplo: get_by_usuario(5)
        """
        return Mantenimiento.objects.filter(usuario_id=id_usuario)

    @staticmethod
    def get_by_tipo(tipo_mantenimiento):
        """
        Obtiene mantenimientos filtrando por tipo.
        Ejemplo: get_by_tipo('preventivo')
        """
        return Mantenimiento.objects.filter(tipo_mantenimiento=tipo_mantenimiento)

    @staticmethod
    def get_programados():
        """Retorna todos los mantenimientos programados."""
        return Mantenimiento.objects.filter(tipo_mantenimiento='programado')

    @staticmethod
    def get_correctivos():
        """Retorna todos los mantenimientos correctivos."""
        return Mantenimiento.objects.filter(tipo_mantenimiento='correctivo')

    @staticmethod
    def get_by_fecha(fecha):
        """
        Obtiene los mantenimientos realizados en una fecha específica.
        Ejemplo: get_by_fecha('2024-01-05')
        """
        return Mantenimiento.objects.filter(fecha_mantenimiento=fecha)


    @staticmethod
    def get_between_fechas(fecha_inicio, fecha_fin):
        """
        Obtiene mantenimientos entre dos fechas.
        Ejemplo:
        get_between_fechas('2024-01-01', '2024-01-31')
        """
        return Mantenimiento.objects.filter(
            fecha_mantenimiento__range=(fecha_inicio, fecha_fin)
        )

    @staticmethod
    def search(descripcion):
        """
        Busca mantenimientos por coincidencias parciales en la descripción.
        Ejemplo: search('aceite')
        """
        return Mantenimiento.objects.filter(descripcion__icontains=descripcion)

    @staticmethod
    def get_costos_mayores_a(valor):
        """
        Obtiene mantenimientos cuyo costo es mayor a un valor dado.
        Ejemplo: get_costos_mayores_a(500000)
        """
        return Mantenimiento.objects.filter(costo__gt=valor)

    @staticmethod
    def get_ultimo_por_maquina_y_tipo(id_maquina: int, tipo_mantenimiento: str):
        """
        Obtiene el último mantenimiento registrado de un tipo específico
        para una máquina.
        
        Ejemplo:
            get_ultimo_por_maquina_y_tipo(5, 'preventivo')
        
        Retorna None si no existe.
        """
        try:
            return Mantenimiento.objects.filter(
                maquina_id=id_maquina,
                tipo_mantenimiento=tipo_mantenimiento
            ).order_by('-fecha_mantenimiento').first()
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_ultimo_por_maquina_y_programado(id_maquina: int, id_programado: int):
        """
        Obtiene el último mantenimiento realizado a una máquina según
        un mantenimiento programado específico.

        Parámetros:
            id_maquina (int): ID de la máquina.
            id_programado (int): ID del mantenimiento programado.

        Retorna:
            Mantenimiento | None: El registro más reciente o None si no existe.
        """
        return (
            Mantenimiento.objects
            .filter(maquina_id=id_maquina, programado_id=id_programado)
            .order_by('-fecha_mantenimiento')
            .first()
        )