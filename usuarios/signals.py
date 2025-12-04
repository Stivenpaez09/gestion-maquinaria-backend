from django.db.models.signals import post_migrate
from django.dispatch import receiver

from usuarios.models.usuario import Usuario
from usuarios.services.usuario_service import UsuarioService


@receiver(post_migrate)
def crear_usuario_predeterminado(sender, **kwargs):
    if sender.label != "usuarios":  # aseguramos que es el módulo usuarios
        return

    try:
        if Usuario.objects.filter(id_usuario=1).exists():
            return
    except Exception:
        return

    usuario =  {
        "nombre": "Usuario General",
        "cargo" : "Gerente",
        "email" : "admin@servimacons.com",
        "telefono" : "3000000000"
    }

    service = UsuarioService()
    service.crear_usuario(data=usuario)

    print("Usuario predeterminado creado correctamente.")