from datetime import date

from django.core.validators import EmailValidator, RegexValidator
from rest_framework import serializers
from usuarios.models.usuario import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id_usuario',
            'nombre',
            'cargo',
            'email',
            'telefono',
            'fecha_ingreso',
            'foto',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ('id_usuario', 'created_at', 'updated_at')

        extra_kwargs = {
            'nombre': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': "El nombre es obligatorio.",
                    'blank': "El nombre no puede estar vacío.",
                    'null': "El nombre no puede ser nulo.",
                    'invalid': "Formato inválido para el nombre."
                },
                'validators': [
                    RegexValidator(
                        regex=r'^.{3,100}$',
                        message="El nombre debe tener entre 3 y 100 caracteres."
                    )
                ]
            },
            'cargo': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': "El cargo es obligatorio.",
                    'blank': "El cargo no puede estar vacío.",
                    'null': "El cargo no puede ser nulo.",
                    'invalid': "Formato inválido para el cargo."
                },
                'validators': [
                    RegexValidator(
                        regex=r'^.{1,100}$',
                        message="El cargo debe tener máximo 100 caracteres."
                    )
                ]
            },
            'email': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': "El correo electrónico es obligatorio.",
                    'invalid': "Correo electrónico inválido.",
                    'blank': "El correo electrónico no puede estar vacío.",
                    'null': "El correo electrónico no puede ser nulo."
                },
                'validators': [
                    EmailValidator(message="Correo electrónico inválido.")
                ]
            },
            'telefono': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': "El número de teléfono es obligatorio.",
                    'invalid': "El teléfono debe contener solo números.",
                    'blank': "El teléfono no puede estar vacío.",
                    'null': "El teléfono no puede ser nulo."
                },
                'validators': [
                    RegexValidator(
                        regex=r'^\d{7,15}$',
                        message="El teléfono debe contener entre 7 y 15 dígitos numéricos."
                    )
                ]
            },
            'fecha_ingreso': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    'required': "La fecha de ingreso es obligatoria.",
                    'invalid': "La fecha debe tener formato YYYY-MM-DD.",
                    'null': "La fecha de ingreso no puede ser nula."
                },
                'validators': [
                    RegexValidator(
                        regex=r'^\d{4}-\d{2}-\d{2}$',
                        message="La fecha debe tener formato YYYY-MM-DD."
                    )
                ]
            },
            'foto': {
                'required': False,
                'allow_null': True,
                'error_messages': {
                    'invalid': "La foto debe ser un archivo de imagen válido."
                }
            }
        }


    # ---------------------------------------------------------
    # Validación adicional
    # ---------------------------------------------------------
    def validate(self, attrs):
        """
        Validaciones cruzadas o de reglas de negocio.
        Aquí evitamos tocar extra_kwargs.
        """
        fecha_ingreso = attrs.get('fecha_ingreso')

        # Ejemplo: no permitir fechas futuras
        if fecha_ingreso and fecha_ingreso > date.today():
            raise serializers.ValidationError({
                "fecha_ingreso": "La fecha de ingreso no puede ser futura."
            })

        return attrs