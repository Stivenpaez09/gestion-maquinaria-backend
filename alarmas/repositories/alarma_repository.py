from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.utils.timezone import now

from alarmas.models.alarma import Alarma


class AlarmaRepository:
    """
    Repositorio para el modelo Alarma.
    Encapsula todas las operaciones CRUD y consultas personalizadas
    relacionadas con alarmas de máquinas, incluyendo búsquedas,
    filtrados, estadísticas y validaciones lógicas.
    """

    @staticmethod
    def get_all():
        """Retorna todas las alarmas."""
        return Alarma.objects.all()

    @staticmethod
    def get_by_id(**kwargs):
        """
        Obtiene una alarma por cualquier campo.
        Ejemplo: get_by_id(id_alarma=10)
        Retorna None si no existe.
        """
        try:
            return Alarma.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create(**kwargs):
        """
        Crea una nueva alarma en la base de datos.
        Ejemplo:
        create(maquina=obj, tipo='mantenimiento', nivel='alta')
        """
        return Alarma.objects.create(**kwargs)

    @staticmethod
    def update(id_alarma, **kwargs):
        """
        Actualiza una alarma por su ID.
        Ejemplo: update(1, vista=True)
        """
        alarma = AlarmaRepository.get_by_id(id_alarma=id_alarma)
        if not alarma:
            return None

        for key, value in kwargs.items():
            setattr(alarma, key, value)

        alarma.save()
        return alarma

    @staticmethod
    def delete(id_alarma):
        """
        Elimina una alarma por su ID.
        Ejemplo: delete(1)
        Retorna True si fue eliminada, False si no existe.
        """
        alarma = AlarmaRepository.get_by_id(id_alarma=id_alarma)
        if not alarma:
            return False

        alarma.delete()
        return True

    # =====================================================
    # CONSULTAS POR CAMPOS
    # =====================================================

    @staticmethod
    def get_by_maquina(id_maquina):
        """Retorna todas las alarmas asociadas a una máquina."""
        return Alarma.objects.filter(maquina_id=id_maquina)

    @staticmethod
    def get_by_tipo(tipo):
        """Filtra alarmas por tipo."""
        return Alarma.objects.filter(tipo=tipo)

    @staticmethod
    def get_by_nivel(nivel):
        """Filtra alarmas por nivel de severidad."""
        return Alarma.objects.filter(nivel=nivel)

    @staticmethod
    def get_no_vistas():
        """Retorna alarmas que aún no han sido vistas."""
        return Alarma.objects.filter(vista=False)

    @staticmethod
    def get_vistas():
        """Retorna alarmas ya revisadas."""
        return Alarma.objects.filter(vista=True)

    @staticmethod
    def get_criticas():
        """Retorna todas las alarmas de nivel crítico."""
        return Alarma.objects.filter(nivel="crítica")

    @staticmethod
    def get_no_vistas_by_maquina(id_maquina):
        """Retorna alarmas no vistas para una máquina específica."""
        return Alarma.objects.filter(maquina_id=id_maquina, vista=False)

    @staticmethod
    def get_activas_by_tipo_and_maquina(tipo, id_maquina):
        """
        Retorna alarmas activas (no vistas) del mismo tipo para una máquina.
        Útil para evitar duplicados.
        """
        return Alarma.objects.filter(
            maquina_id=id_maquina,
            tipo=tipo,
            vista=False
        )

    # =====================================================
    # CONSULTAS POR FECHAS
    # =====================================================

    @staticmethod
    def get_by_fecha(fecha):
        """Obtiene alarmas registradas en una fecha específica."""
        return Alarma.objects.filter(fecha_registro__date=fecha)

    @staticmethod
    def get_between_fechas(fecha_inicio, fecha_fin):
        """Retorna alarmas entre dos fechas."""
        return Alarma.objects.filter(
            fecha_registro__range=(fecha_inicio, fecha_fin)
        )

    @staticmethod
    def get_recientes(horas=24):
        """
        Retorna alarmas generadas en las últimas X horas.
        Por defecto: últimas 24 horas.
        """
        """Obtiene alarmas registradas en las últimas N horas."""
        fecha_limite = now() - timedelta(hours=horas)
        return Alarma.objects.filter(fecha_registro__gte=fecha_limite)

    # =====================================================
    # BÚSQUEDAS AVANZADAS (TEXTO)
    # =====================================================

    @staticmethod
    def search_descripcion(texto):
        """Busca alarmas por texto parcial en la descripción."""
        return Alarma.objects.filter(descripcion__icontains=texto)

    # =====================================================
    # CONSULTAS PARA DASHBOARD
    # =====================================================

    @staticmethod
    def contar_por_nivel():
        """Retorna un diccionario con conteos por nivel de severidad."""
        return Alarma.objects.values('nivel').annotate(count=Count('id_alarma'))

    @staticmethod
    def contar_por_tipo():
        """Retorna un diccionario con conteos por tipo de alarma."""
        return Alarma.objects.values('tipo').annotate(count=Count('id_alarma'))

    @staticmethod
    def contar_no_vistas():
        """Retorna el total de alarmas no vistas."""
        return Alarma.objects.filter(vista=False).count()

    @staticmethod
    def get_ultimas(limit=10):
        """Retorna las últimas N alarmas registradas."""
        return Alarma.objects.order_by('-fecha_registro')[:limit]

    @staticmethod
    def get_agrupadas_por_maquina():
        """Retorna alarmas agrupadas por máquina."""
        return Alarma.objects.values('maquina_id').annotate(count=Count('id_alarma'))