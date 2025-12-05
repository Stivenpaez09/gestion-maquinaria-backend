from django.db import models

from maquinarias.models.maquinaria import Maquinaria


class MantenimientoProgramado(models.Model):
    """
    Modelo que representa un mantenimiento programado de una maquinaria.
    Contiene el tipo de mantenimiento, su intervalo en horas de uso,
    descripción y la maquinaria asociada.
    """

    id_programado = models.AutoField(primary_key=True)

    maquina = models.ForeignKey(
        Maquinaria,
        on_delete=models.CASCADE,
        db_column='id_maquina',
        related_name='mantenimientos_programados'
    )

    nombre = models.CharField(
        max_length=100,
        default='General',
        help_text="Nombre del mantenimiento programado (único por máquina)"
    )

    tipo = models.CharField(
        max_length=50,
        choices=[
            ('preventivo', 'Preventivo'),
            ('predictivo', 'Predictivo'),
        ],
        help_text="Ejemplo: Preventivo, predictivo"
    )

    intervalo_horas = models.PositiveIntegerField(
        help_text="Horas de uso entre cada mantenimiento programado"
    )

    descripcion = models.TextField(
        null=True,
        blank=True,
        help_text="Detalles adicionales del mantenimiento"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mantenimientos_programados'
        verbose_name = "Mantenimiento programado"
        verbose_name_plural = "Mantenimientos programados"
        ordering = ['id_programado']

        constraints = [
            models.UniqueConstraint(
                fields=['maquina', 'nombre'],
                name='unique_nombre_por_maquina'
            )
        ]

    def __str__(self):
        return f"{self.tipo} - cada {self.intervalo_horas}h"