from rest_framework.permissions import BasePermission

from logins.permissions.permisos_por_rol import ROLE_PERMISSIONS


class RolPermission(BasePermission):

    PUBLIC_ACTIONS = {"autenticar"}

    def has_permission(self, request, view):
        action = getattr(view, 'action', None)

        if action in self.PUBLIC_ACTIONS:
            return True

        permission_key = getattr(view, 'permission_key', None)
        if not permission_key:
            return False

        permiso_necesario = f"{permission_key}:{action}"

        token = getattr(request, "auth", None)

        rol = None
        if token:
            # SimpleJWT
            try:
                rol = token.get("rol")
            except:
                pass

        if not rol:
            return False

        permisos_rol = ROLE_PERMISSIONS.get(rol, set())
        return permiso_necesario in permisos_rol
