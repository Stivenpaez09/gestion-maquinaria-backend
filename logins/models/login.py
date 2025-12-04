from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from logins.models.login_manager import LoginManager
from usuarios.models.usuario import Usuario


class Login(AbstractBaseUser, PermissionsMixin):
    """
    Modelo profesional para gestionar las credenciales de acceso
    asociadas a un Usuario. Define roles, username y contraseña
    en formato seguro (hash).
    """

    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('ASISTENTE', 'Asistente'),
        ('RESPONSABLE_DE_MANTENIMIENTO', 'Responsable de mantenimiento'),
        ('OPERADOR', 'Operador'),
        ('TECNICO_DE_MANTENIMIENTO', 'Tecnico de mantenimiento'),
    ]

    id_login = models.AutoField(primary_key=True)

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='credenciales',
        null=True,
        blank=True
    )

    username = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False
    )

    password = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    rol = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='OPERADOR'
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = LoginManager()
    class Meta:
        db_table = "logins"
        verbose_name = "Login"
        verbose_name_plural = "Logins"

    # --- Métodos especiales ---
    def set_password(self, raw_password):
        super().set_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        """Verifica la contraseña contra el hash almacenado."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.username} ({self.rol})"