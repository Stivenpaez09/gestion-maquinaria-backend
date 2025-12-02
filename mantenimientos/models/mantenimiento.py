from django.db import models

from mantenimientos_programados.models.mantenimiento_programado import MantenimientoProgramado
from maquinarias.models.maquinaria import Maquinaria
from usuarios.models.usuario import Usuario


class Mantenimiento(models.Model):
    id_mantenimiento = models.AutoField(primary_key=True)

    maquina = models.ForeignKey(
        Maquinaria,
        on_delete=models.CASCADE,
        db_column='id_maquina',
        related_name='mantenimientos_maquina'
    )

    programado = models.ForeignKey(
        MantenimientoProgramado,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_programado',
        related_name='mantenimientos_programados'
    )

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario',
        related_name='mantenimientos_usuario'
    )

    tipo_mantenimiento = models.CharField(
        max_length=20,
        choices=[
            ('preventivo', 'Preventivo'),
            ('correctivo', 'Correctivo'),
            ('predictivo', 'Predictivo'),
        ],
        help_text="Tipo de mantenimiento realizado."
    )

    descripcion = models.TextField()

    fecha_mantenimiento = models.DateField()

    horas_realizadas = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Horas totales acumuladas de la máquina al momento del mantenimiento."
    )

    costo = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mantenimientos'
        verbose_name = "Mantenimiento"
        verbose_name_plural = "Mantenimientos"

    def __str__(self):
        return f"Mantenimiento #{self.id_mantenimiento} - {self.tipo_mantenimiento}"
