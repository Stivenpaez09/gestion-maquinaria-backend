from django.db import models



class Usuario(models.Model):
    """
    Modelo profesional para la gestión de usuarios.
    Almacena información personal, laboral y la ruta física de su foto.
    """

    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    fecha_ingreso = models.DateField(null=True, blank=True)
    foto = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "usuarios"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.nombre} ({self.email})"