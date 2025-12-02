from datetime import date

from rest_framework import serializers
from django.core.validators import RegexValidator
from maquinarias.models.maquinaria import Maquinaria

class MaquinariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maquinaria
        fields = [
            'id_maquina',
            'nombre_maquina',
            'modelo',
            'marca',
            'serie',
            'fecha_adquisicion',
            'horas_totales',
            'estado',
            'foto',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ('id_maquina', 'created_at', 'updated_at')

        extra_kwargs = {
            'nombre_maquina': {
                'required': True,
                'allow_null': False,
                'allow_blank': False,
                'error_messages': {
                    'required': "El nombre de la máquina es obligatorio.",
                    'blank': "El nombre de la máquina no puede estar vacío.",
                },
                'validators': [
                    RegexValidator(
                        regex=r'^.{3,100}$',
                        message="El nombre de la máquina debe tener entre 3 y 100 caracteres."
                    )
                ]
            },
            'modelo': {
                'required': True,
                'allow_null': False,
                'allow_blank': False,
                'error_messages': {
                    'required': "El modelo es obligatorio.",
                    'blank': "El modelo no puede estar vacío.",
                },
                'validators': [
                    RegexValidator(
                        regex=r'^.{2,100}$',
                        message="El modelo debe tener entre 2 y 100 caracteres."
                    )
                ]
            },
            'marca': {
                'required': True,
                'allow_null': False,
                'allow_blank': False,
                'error_messages': {
                    'required': "La marca es obligatoria.",
                    'blank': "La marca no puede estar vacía.",
                },
                'validators': [
                    RegexValidator(
                        regex=r'^.{2,100}$',
                        message="La marca debe tener entre 2 y 100 caracteres."
                    )
                ]
            },
            'serie': {
                'required': True,
                'allow_null': False,
                'allow_blank': False,
                'error_messages': {
                    'required': "La serie es obligatoria.",
                    'blank': "La serie no puede estar vacía.",
                },
                'validators': [
                    RegexValidator(
                        regex=r'^.{3,100}$',
                        message="La serie debe tener entre 3 y 100 caracteres."
                    )
                ]
            },

            # -------------------------------------------
            # DATEFIELD OBLIGATORIO (NO ALLOW_BLANK)
            # -------------------------------------------
            'fecha_adquisicion': {
                'required': True,
                'allow_null': False,  # correcto
                # NO allow_blank aquí (haría CRASH)
                'error_messages': {
                    'required': "La fecha de adquisición es obligatoria.",
                    'invalid': "La fecha debe tener formato YYYY-MM-DD."
                }
            },

            # -------------------------------------------
            # DECIMALFIELD OBLIGATORIO (NO allow_blank)
            # -------------------------------------------
            'horas_totales': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    'required': "El número de horas totales es obligatorio.",
                    'invalid': "Las horas totales deben ser un número válido."
                }
            },

            # -------------------------------------------
            # CHOICEFIELD OBLIGATORIO
            # -------------------------------------------
            'estado': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    'required': "El estado de la máquina es obligatorio.",
                    'invalid_choice': "El estado debe ser uno válido.",
                }
            }
        }

    def validate_fecha_adquisicion(self, value):
        """La fecha de adquisición no puede ser futura."""
        if value > date.today():
            raise serializers.ValidationError("La fecha de adquisición no puede ser futura.")
        return value

    def validate_horas_totales(self, value):
        """Las horas totales no pueden ser negativas."""
        if value < 0:
            raise serializers.ValidationError("Las horas totales deben ser un número positivo.")
        if value > 99999999.99:
            raise serializers.ValidationError("El valor de horas es demasiado grande.")
        return value

    def validate_estado(self, value):
        """Valida que el estado sea consistente."""
        estados_validos = ['operativa', 'en mantenimiento', 'fuera de servicio']
        if value not in estados_validos:
            raise serializers.ValidationError("Estado inválido.")
        return value

    def validate(self, data):
        """
        Validaciones cruzadas:
        - Una máquina no puede estar 'operativa' si horas_totales es 0.
        - La fecha de adquisición debe ser coherente.
        """
        fecha = data.get("fecha_adquisicion")
        horas = data.get("horas_totales")
        estado = data.get("estado")

        if estado == "operativa" and horas == 0:
            raise serializers.ValidationError({
                "horas_totales": "Una máquina operativa debe tener más de 0 horas de uso."
            })

        if fecha and fecha > date.today():
            raise serializers.ValidationError({
                "fecha_adquisicion": "La fecha de adquisición no puede ser futura."
            })

        return data