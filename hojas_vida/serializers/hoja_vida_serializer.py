from django.core.validators import RegexValidator
from django.utils import timezone
from rest_framework import serializers

from hojas_vida.models.hoja_vida import HojaVida
from maquinarias.models.maquinaria import Maquinaria
from usuarios.models.usuario import Usuario


class HojaVidaSerializer(serializers.ModelSerializer):
    """
    Serializer profesional para la gestión de hojas de vida.
    Incluye validaciones estrictas para los campos,
    asegurando integridad referencial y formato correcto
    de la información almacenada.
    """

    class Meta:
        model = HojaVida
        fields = [
            'id_hoja',
            'maquinaria',
            'usuario',
            'descripcion',
            'archivo',
            'fecha_registro',
            'created_at',
            'updated_at'
        ]

        # Campos que no deben modificarse manualmente
        read_only_fields = ('id_hoja', 'created_at', 'updated_at')

        # Validaciones y reglas de negocio por campo
        extra_kwargs = {
             'maquinaria': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    "required": "Debe especificar la maquinaria asociada.",
                    "null": "La maquinaria no puede ser nula."
                }
            },
            'usuario': {
                'required': False,
                'allow_null': True
            },
            'descripcion': {
                'required': False,
                'allow_blank': True,
                'validators': [
                    RegexValidator(
                        regex=r'^.{0,2000}$',
                        message="La descripción puede tener máximo 2000 caracteres"
                    )
                ]
            },
            'archivo': {
                'required': False,
                'allow_blank': True,
                'validators': [
                    RegexValidator(
                        regex=r'^.{0,255}$',
                        message="La ruta del archivo debe tener máximo 255 caracteres"
                    )
                ]
            },
            'fecha_registro': {
                'required': False,
                'validators': [
                    RegexValidator(
                        regex=r'^\d{4}-\d{2}-\d{2}$',
                        message="La fecha debe tener formato YYYY-MM-DD"
                    )
                ]
            }
        }


    def validate_maquinaria(self, value):
        """Valida que la maquinaria exista."""
        if not Maquinaria.objects.filter(id_maquina=value.id_maquina).exists():
            raise serializers.ValidationError("La maquinaria indicada no existe.")
        return value

    def validate_usuario(self, value):
        """Valida que el usuario exista si se envía."""
        if value is not None and not Usuario.objects.filter(id_usuario=value.id_usuario).exists():
            raise serializers.ValidationError("El usuario indicado no existe.")
        return value

    def validate_fecha_registro(self, value):
        """Valida que la fecha de registro no sea futura."""
        if value > timezone.now().date():
            raise serializers.ValidationError("La fecha de registro no puede ser en el futuro.")
        return value
