from django.db import models


class Empresa(models.Model):
    """
    Modelo profesional para la gestión de empresas.
    Almacena información básica y de identificación tributaria
    de una empresa en Colombia.
    """

    id_empresa = models.AutoField(primary_key=True)

    nombre = models.CharField(max_length=150)
    nit = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    departamento = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=120, null=True, blank=True)
    representante_legal = models.CharField(max_length=150, null=True, blank=True)
    sector = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "empresas"
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return f"{self.nombre} - NIT: {self.nit}-{self.digito_verificacion}"