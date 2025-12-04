from django.contrib.auth.base_user import BaseUserManager


class LoginManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("El nombre de usuario es obligatorio")

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(username=username, **extra_fields)

        if password:
            user.set_password(password)
        else:
            raise ValueError("La contraseña es obligatoria para crear un usuario")  # opcional según tu caso

        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("rol", "ADMIN")

        return self.create_user(username, password, **extra_fields)