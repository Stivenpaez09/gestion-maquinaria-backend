from django.db import models

from maquinarias.models.maquinaria import Maquinaria
from proyectos.models.proyecto import Proyecto
from usuarios.models.usuario import Usuario


class RegistroHorasMaquinaria(models.Model):
    id_registro = models.AutoField(primary_key=True)

    maquina = models.ForeignKey(
        Maquinaria,
        on_delete=models.CASCADE,
        db_column='id_maquina',
        related_name='registros_maquina'
    )

    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_proyecto',
        related_name='registros_proyecto'
    )

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario',
        related_name='registros_usuario'
    )

    fecha = models.DateField(
        help_text="Fecha en que se registraron las horas trabajadas."
    )

    horas_trabajadas = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Número de horas trabajadas por la máquina en esa fecha."
    )

    observaciones = models.TextField(
        null=True,
        blank=True,
        help_text="Observaciones adicionales sobre el registro."
    )

    foto_planilla = models.URLField(max_length=500, blank=True, null=True)
    foto_horometro_inicial = models.URLField(max_length=500, blank=True, null=True)
    foto_horometro_final = models.URLField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'registros_horas_maquinaria'
        verbose_name = "registro_horas_maquinaria"
        verbose_name_plural = "registros_horas_maquinaria"

    def __str__(self):
        return f"Registro #{self.id_registro} - Máquina #{self.maquina.id_maquina} - {self.fecha}"