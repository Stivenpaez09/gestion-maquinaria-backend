from django.db.models.signals import post_migrate
from django.dispatch import receiver

from logins.models import Login
from logins.services.login_service import LoginService
from usuarios.models.usuario import Usuario


@receiver(post_migrate)
def crear_usuario_predeterminado(sender, **kwargs):

    # Asegurar que solo se ejecute cuando la app 'logins' termina de migrar
    if sender.label != "logins":
        return

    # Evitar consultar la tabla si aún no existe
    try:
        if Login.objects.filter(username="admin_servimacons").exists():
            return
    except Exception:
        # La tabla aún no existe; no intentar crear el usuario todavía
        return

    try:
        usuario = Usuario.objects.filter(id_usuario=1).first()
        if not usuario:
            print("El usuario predeterminado aún no existe. No se crea el login.")
            return
    except Exception:
        return

    # Datos del usuario predeterminado
    login = {
        "usuario": 1,
        "username": "admin_servimacons",
        "password": "admin123*",
        "rol": "ADMIN",
        "is_active": True
    }

    service = LoginService()
    service.crear_login(data=login)
