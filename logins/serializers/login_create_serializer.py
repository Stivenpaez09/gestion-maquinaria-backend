from django.core.validators import RegexValidator
from rest_framework import serializers

from logins.models.login import Login


class LoginCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = [
            'id_login',
            'usuario',
            'username',
            'password',
            'rol',
            'is_active',
            'created_at',
            'updated_at'
        ]

        read_only_fields = (
            'id_login',
            'created_at',
            'updated_at'
        )

        extra_kwargs = {
            'username': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': "El username es obligatorio.",
                    'blank': "El username no puede estar vacío.",
                    'null': "El username no puede ser nulo.",
                    'invalid': "Formato inválido para el username."
                },
                'validators': [
                    RegexValidator(
                        regex=r'^[a-zA-Z0-9_.-]{4,50}$',
                        message="El username debe tener entre 4 y 50 caracteres y solo puede contener letras, números y _ . -"
                    )
                ]
            },
            'password': {
                'required': True,
                'write_only': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': "La contraseña es obligatoria.",
                    'blank': "La contraseña no puede estar vacía.",
                    'null': "La contraseña no puede ser nula.",
                    'invalid': "Formato inválido para la contraseña."
                },
                'validators': [
                    RegexValidator(
                        regex=r'^.{8,255}$',
                        message="La contraseña debe tener al menos 8 caracteres."
                    )
                ]
            },
            'rol': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': "El rol es obligatorio.",
                    'blank': "El rol no puede estar vacío.",
                    'null': "El rol no puede ser nulo.",
                    'invalid': "Rol inválido."
                }
            },
            'usuario': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    'required': "El usuario asociado es obligatorio.",
                    'null': "El usuario no puede ser nulo.",
                    'invalid': "ID de usuario inválido."
                }
            }
        }

