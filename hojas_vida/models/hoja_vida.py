from django.db import models
from django.utils import timezone

from maquinarias.models.maquinaria import Maquinaria
from usuarios.models.usuario import Usuario


class HojaVida(models.Model):
    """
    Modelo profesional para gestionar las hojas de vida de una maquinaria.
    Cada registro contiene información documental y referencias a la máquina
    y al usuario que realizó el registro.
    """

    id_hoja = models.AutoField(primary_key=True)
    maquinaria = models.ForeignKey(
        Maquinaria,
        on_delete=models.CASCADE,
        db_column="id_maquina",
        related_name="hojas_vida"
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        db_column="id_usuario",
        related_name="hojas_vida_registradas"
    )

    descripcion = models.TextField(null=True, blank=True)

    archivo = models.CharField(max_length=500, null=True, blank=True)

    fecha_registro = models.DateField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hoja_vida"
        verbose_name = "Hoja de Vida"
        verbose_name_plural = "Hojas de Vida"

    def __str__(self):
        return f"Hoja de Vida #{self.id_hoja} - Máquina {self.descripcion}"