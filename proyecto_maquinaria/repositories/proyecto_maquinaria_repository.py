from django.core.exceptions import ObjectDoesNotExist

from proyecto_maquinaria.models.proyecto_maquinaria import ProyectoMaquinaria


class ProyectoMaquinariaRepository:
    """
    Repositorio para el modelo ProyectoMaquinaria.
    Encapsula todas las operaciones CRUD y consultas personalizadas
    sobre la base de datos.
    """

    @staticmethod
    def get_all():
        """Retorna todas las asignaciones de máquinas a proyectos."""
        return ProyectoMaquinaria.objects.all()

    @staticmethod
    def get_by_id(**kwargs):
        """
        Busca una asignación por cualquier campo.
        Ejemplo: get_by_id(id_proyecto_maquinaria=1)
        Retorna None si no existe.
        """
        try:
            return ProyectoMaquinaria.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create(**kwargs):
        """
        Crea una nueva asignación de máquina a proyecto.
        Ejemplo:
        create(
            proyecto=proyecto_obj,
            maquina=maquina_obj,
            horas=100,
            finalizado=False
        )
        """
        asignacion = ProyectoMaquinaria.objects.create(**kwargs)
        return asignacion

    @staticmethod
    def update(id_proyecto_maquinaria, **kwargs):
        """
        Actualiza una asignación por su ID.
        Ejemplo: update(1, finalizado=True)
        Retorna la asignación actualizada o None si no existe.
        """
        asignacion = ProyectoMaquinariaRepository.get_by_id(id_proyecto_maquinaria=id_proyecto_maquinaria)
        if not asignacion:
            return None

        for key, value in kwargs.items():
            setattr(asignacion, key, value)

        asignacion.save()
        return asignacion

    @staticmethod
    def update_horas_acumuladas(proyecto_maquinaria: ProyectoMaquinaria, horas_a_sumar ):
        if not proyecto_maquinaria or not isinstance(proyecto_maquinaria, ProyectoMaquinaria):
            return None

        proyecto_maquinaria.horas_acumuladas += horas_a_sumar
        proyecto_maquinaria.save()
        return proyecto_maquinaria



    @staticmethod
    def delete(id_proyecto_maquinaria):
        """
        Elimina una asignación por su ID.
        Ejemplo: delete(1)
        Retorna True si se eliminó correctamente, False si no existe.
        """
        asignacion = ProyectoMaquinariaRepository.get_by_id(id_proyecto_maquinaria=id_proyecto_maquinaria)
        if not asignacion:
            return False

        asignacion.delete()
        return True

    @staticmethod
    def get_by_proyecto(id_proyecto):
        """
        Obtiene todas las asignaciones asociadas a un proyecto.
        Ejemplo: get_by_proyecto(3)
        """
        return ProyectoMaquinaria.objects.filter(proyecto_id=id_proyecto)

    @staticmethod
    def get_by_maquina(id_maquina):
        """
        Obtiene todas las asignaciones de un proyecto asociadas a una máquina.
        Ejemplo: get_by_maquina(5)
        """
        return ProyectoMaquinaria.objects.filter(maquina_id=id_maquina)

    @staticmethod
    def get_activos():
        """
        Retorna todas las asignaciones que no han sido finalizadas.
        """
        return ProyectoMaquinaria.objects.filter(finalizado=False)

    @staticmethod
    def get_finalizados():
        """
        Retorna todas las asignaciones finalizadas.
        """
        return ProyectoMaquinaria.objects.filter(finalizado=True)

    @staticmethod
    def get_activos_by_maquina(id_maquina):
        """
        Retorna todas las asignaciones activas de una máquina específica.
        """
        return ProyectoMaquinaria.objects.filter(maquina_id=id_maquina, finalizado=False)

    @staticmethod
    def get_finalizados_by_proyecto(id_proyecto):
        """
        Retorna todas las asignaciones finalizadas de un proyecto específico.
        """
        return ProyectoMaquinaria.objects.filter(proyecto_id=id_proyecto, finalizado=True)

    @staticmethod
    def get_last_by_maquina(id_maquina: int):
        """
        Obtiene el último registro de proyecto_maquinaria para una máquina.
        Ordena por fecha descendente.
        
        Ejemplo:
            get_ultimo_por_maquina(5)
        
        Retorna None si no existe.
        """
        try:
            return ProyectoMaquinaria.objects.filter(
                maquina_id=id_maquina
            ).order_by('-fecha_creacion').first()
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def search_by_horas(min_horas=None, max_horas=None):
        """
        Busca asignaciones filtrando por horas TOTALES pactadas.
        Ejemplo: search_by_horas(min_horas=50, max_horas=200)
        """
        queryset = ProyectoMaquinaria.objects.all()

        if min_horas is not None:
            queryset = queryset.filter(horas_totales__gte=min_horas)

        if max_horas is not None:
            queryset = queryset.filter(horas_totales__lte=max_horas)

        return queryset