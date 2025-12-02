from rest_framework import serializers
from django.core.validators import RegexValidator
from conductores.models.conductor import Conductor


class ConductorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conductor
        fields = [
            'id_conductor',
            'usuario',
            'licencia',
            'fecha_vencimiento',
            'licencia_vencida',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ('id_conductor', 'created_at', 'updated_at')

        extra_kwargs = {
            'usuario': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    'required': "El usuario es obligatorio.",
                    'null': "El usuario no puede ser nulo.",
                    'invalid': "El usuario es inválido."
                }
            },
            'licencia': {
                'required': True,
                'allow_null': False,
                'allow_blank': False,
                'error_messages': {
                    'required': "La licencia es obligatoria.",
                    'blank': "La licencia no puede estar vacía.",
                    'null': "La licencia no puede ser nula.",
                    'invalid': "Formato inválido para la licencia."
                },
                'validators': [
                    RegexValidator(
                        regex=r'^.{3,50}$',
                        message="La licencia debe tener entre 3 y 50 caracteres."
                    )
                ]
            },
            'fecha_vencimiento': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    'required': "La fecha de vencimiento es obligatoria.",
                    'null': "La fecha de vencimiento no puede ser nula.",
                    'invalid': "La fecha debe tener un formato YYYY-MM-DD."
                }
            },
            'licencia_vencida': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    'required': "Debe especificar si la licencia está vencida.",
                    'null': "El campo licencia_vencida no puede ser nulo.",
                    'invalid': "Valor inválido para licencia_vencida."
                }
            }
        }

    def validate_fecha_vencimiento(self, value):
        """Valida que la fecha de vencimiento no sea pasada."""
        from datetime import date

        if value < date.today():
            raise serializers.ValidationError(
                "La fecha de vencimiento no puede ser anterior a hoy."
            )

        return value

    def validate(self, data):
        """
        Validaciones cruzadas:
        - Si la licencia está marcada como vencida pero la fecha es futura, es inconsistente.
        """
        fecha = data.get("fecha_vencimiento")
        vencida = data.get("licencia_vencida")

        from datetime import date

        if fecha and vencida is True and fecha >= date.today():
            raise serializers.ValidationError({
                "licencia_vencida": (
                    "No puede marcar la licencia como vencida si la fecha "
                    "de vencimiento aún no ha pasado."
                )
            })

        return data