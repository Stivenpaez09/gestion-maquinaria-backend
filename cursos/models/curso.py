from django.db import models
from usuarios.models.usuario import Usuario

class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        related_name='cursos'
    )
    nombre_curso = models.CharField(max_length=150)
    institucion = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cursos'
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.nombre_curso