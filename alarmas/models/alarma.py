from django.db import models

from maquinarias.models.maquinaria import Maquinaria


class Alarma(models.Model):
    """
    Modelo profesional para la gestión de alarmas generadas por una máquina.
    Representa avisos automáticos o manuales asociados a un equipo, como
    alarmas de mantenimiento, proyecto o estados críticos.
    """

    id_alarma = models.AutoField(primary_key=True)

    maquina = models.ForeignKey(
        Maquinaria,
        on_delete=models.CASCADE,
        db_column='id_maquina',
        related_name='alarmas',
        help_text="Máquina asociada a la alarma."
    )

    descripcion = models.TextField(
        null=True,
        blank=True,
        help_text="Descripción detallada de la causa o información de la alarma."
    )

    tipo = models.CharField(
        max_length=50,
        help_text="Tipo de alarma: 'mantenimiento', 'proyecto', etc."
    )

    nivel = models.CharField(
        max_length=20,
        default='baja',
        choices=[
            ('baja', 'Baja'),
            ('media', 'Media'),
            ('alta', 'Alta'),
            ('crítica', 'Crítica'),
        ],
        help_text="Nivel de severidad de la alarma."
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        db_column='fecha_registro',
        help_text="Fecha en la que se creó la alarma."
    )

    vista = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación del registro."
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Fecha de última actualización del registro."
    )

    class Meta:
        db_table = 'alarmas'
        verbose_name = "alarma"
        verbose_name_plural = "alarmas"

    def __str__(self):
        return f"Alarma #{self.id_alarma} - {self.tipo} ({self.nivel})"