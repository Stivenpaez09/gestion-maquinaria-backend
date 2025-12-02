from django.core.validators import RegexValidator, EmailValidator
from rest_framework import serializers

from empresas.models.empresa import Empresa


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = [
            'id_empresa',
            'nombre',
            'nit',
            'direccion',
            'ciudad',
            'departamento',
            'telefono',
            'email',
            'representante_legal',
            'sector',
            'created_at',
            'updated_at'
        ]

        read_only_fields = ('id_empresa', 'created_at', 'updated_at')

        extra_kwargs = {
            'nombre': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': "El nombre de la empresa es obligatorio.",
                    'blank': "El nombre no puede estar vacío.",
                    'null': "El nombre no puede ser nulo."
                },
                'validators': [
                    RegexValidator(
                        regex=r'^.{3,150}$',
                        message="El nombre debe tener entre 3 y 150 caracteres."
                    )
                ]
            },

            'nit': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': "El NIT es obligatorio.",
                    'blank': "El NIT no puede estar vacío.",
                    'null': "El NIT no puede ser nulo.",
                    'invalid': "Formato inválido para el NIT."
                },
                'validators': [
                    RegexValidator(
                        regex=r'^\d{5,20}$',
                        message="El NIT debe contener entre 5 y 20 dígitos numéricos."
                    )
                ]
            },

            'direccion': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': "La dirección es obligatoria.",
                    'blank': "La dirección no puede estar vacía.",
                    'null': "La dirección no puede ser nula."
                },
                'validators': [
                    RegexValidator(
                        regex=r'^.{5,200}$',
                        message="La dirección debe tener entre 5 y 200 caracteres."
                    )
                ]
            },

            'ciudad': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': "La ciudad es obligatoria.",
                    'blank': "La ciudad no puede estar vacía.",
                    'null': "La ciudad no puede ser nula."
                }
            },

            'departamento': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': "El departamento es obligatorio.",
                    'blank': "El departamento no puede estar vacío.",
                    'null': "El departamento no puede ser nulo."
                }
            },

            'telefono': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': "El número de teléfono es obligatorio.",
                    'blank': "El teléfono no puede estar vacío.",
                    'null': "El teléfono no puede ser nulo.",
                    'invalid': "El teléfono debe contener solo números."
                },
                'validators': [
                    RegexValidator(
                        regex=r'^\d{7,15}$',
                        message="El teléfono debe contener entre 7 y 15 dígitos."
                    )
                ]
            },

            'email': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': "El correo electrónico es obligatorio.",
                    'blank': "El correo electrónico no puede estar vacío.",
                    'null': "El correo electrónico no puede ser nulo.",
                    'invalid': "Correo electrónico inválido."
                },
                'validators': [
                    EmailValidator(message="Correo electrónico inválido.")
                ]
            },

            'representante_legal': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': "El representante legal es obligatorio.",
                    'blank': "El representante legal no puede estar vacío.",
                    'null': "El representante legal no puede ser nulo."
                },
                'validators': [
                    RegexValidator(
                        regex=r'^.{3,150}$',
                        message="El nombre del representante debe tener entre 3 y 150 caracteres."
                    )
                ]
            },

            'sector': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': "El sector económico es obligatorio.",
                    'blank': "El sector no puede estar vacío.",
                    'null': "El sector no puede ser nulo."
                }
            }
        }

    def validate(self, attrs):
        """
        Validaciones de negocio más complejas.
        """

        nombre = attrs.get("nombre")
        nit = attrs.get("nit")

        # ---- 1. Evitar empresas duplicadas por nombre ----
        if Empresa.objects.filter(nombre__iexact=nombre).exists():
            raise serializers.ValidationError({
                "nombre": "Ya existe una empresa registrada con este nombre."
            })

        # ---- 2. Evitar que NITs sospechosos pasen ----
        if nit in ["0000000000", "1111111111", "123456789"]:
            raise serializers.ValidationError({
                "nit": "Este NIT no es válido."
            })

        return attrs