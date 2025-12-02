from django.db import models

from maquinarias.models.maquinaria import Maquinaria
from proyectos.models.proyecto import Proyecto

class ProyectoMaquinaria(models.Model):
    id_proyecto_maquinaria = models.AutoField(primary_key=True)

    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        db_column='id_proyecto',
        related_name='proyectos_maquinas'
    )

    maquina = models.ForeignKey(
        Maquinaria,
        on_delete=models.CASCADE,
        db_column='id_maquina',
        related_name='maquinas_proyectos'
    )

    fecha_asignacion = models.DateField(
        auto_now_add=True,
        help_text="Fecha en que la máquina fue asignada al proyecto."
    )
    horas_totales = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Horas totales pactadas de la máquina."
    )
    horas_acumuladas = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Horas totales pactadas de la máquina."
    )
    finalizado = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'proyecto_maquinaria'
        verbose_name = "Proyecto-Maquinaria"
        verbose_name_plural = "Proyectos-Maquinaria"

    def __str__(self):
        return f"Proyecto #{self.proyecto.id_proyecto} - Máquina #{self.maquina.id_maquina}"
