from django.db import models

class Maquinaria(models.Model):
    id_maquina = models.AutoField(primary_key=True)
    nombre_maquina = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100, null=True, blank=True)
    marca = models.CharField(max_length=100, null=True, blank=True)
    serie = models.CharField(max_length=100, null=True, blank=True)
    fecha_adquisicion = models.DateField(null=True, blank=True)
    horas_totales = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Horas totales de uso de la máquina."
    )

    ESTADOS = [
        ('operativa', 'Operativa'),
        ('en mantenimiento', 'En Mantenimiento'),
        ('fuera de servicio', 'Fuera de Servicio'),
    ]

    estado = models.CharField(
        max_length=50,
        choices=ESTADOS,
        default='operativa'
    )
    foto = models.CharField(max_length=500, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'maquinaria'
        verbose_name = 'Maquinaria'
        verbose_name_plural = 'Maquinarias'

    def __str__(self):
        return f"{self.nombre_maquina} - {self.marca} - {self.modelo}"