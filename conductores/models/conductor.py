from django.db import models
from usuarios.models.usuario import Usuario

class Conductor (models.Model):
    id_conductor = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='conductores'
    )
    licencia = models.CharField(max_length=50)
    fecha_vencimiento = models.DateField()
    licencia_vencida = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'conductores'
        verbose_name = "Conductor"
        verbose_name_plural = "Conductores"

    def __str__(self):
        return f'{self.usuario.nombre} - {self.licencia}'