from rest_framework import serializers

from logins.models.login import Login


class LoginAuthSerializer(serializers.Serializer):
    """
    Serializer para autenticación.
    Solo recibe username y password.
    No está ligado al modelo Login.
    """
    username = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        error_messages={
            'required': 'El nombre de usuario es obligatorio.',
            'null': 'El nombre de usuario no puede ser nulo.',
            'blank': 'El nombre de usuario no puede estar vacío.',
            'invalid': 'El nombre de usuario no tiene un formato válido.'
        }
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        allow_null=False,
        allow_blank=False,
        error_messages={
            'required': 'La contraseña es obligatoria.',
            'null': 'La contraseña no puede ser nula.',
            'blank': 'La contraseña no puede estar vacía.',
            'invalid': 'La contraseña no tiene un formato válido.'
        }
    )