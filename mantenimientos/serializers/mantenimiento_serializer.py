from datetime import date

from django.core.validators import RegexValidator, MinValueValidator
from rest_framework import serializers
from mantenimientos.models.mantenimiento import Mantenimiento

class MantenimientoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mantenimiento
        fields = [
            'id_mantenimiento',
            'programado',
            'maquina',
            'usuario',
            'tipo_mantenimiento',
            'descripcion',
            'fecha_mantenimiento',
            'horas_realizadas',
            'costo',
            'foto',
            'created_at',
            'updated_at'
        ]

        read_only_fields = ('id_mantenimiento', 'created_at', 'updated_at')

        extra_kwargs = {
            'programado': {
                'required': False,
                'allow_null': True
            },
            'usuario': {
                'required': False,
                'allow_null': True
            },
            'foto': {
                'required': False,
                'allow_null': True,
                'allow_blank': True
            },
            'maquina': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    "required": "La máquina es obligatoria.",
                    "null": "La máquina no puede ser nula."
                }
            },

            'tipo_mantenimiento': {
                'required': True,
                'allow_null': False,
                'allow_blank': False,
                'error_messages': {
                    "required": "El tipo de mantenimiento es obligatorio.",
                    "blank": "El tipo de mantenimiento no puede estar vacío.",
                    "null": "El tipo de mantenimiento no puede ser nulo."
                },
                'validators': [
                    RegexValidator(
                        regex=r'^(preventivo|correctivo|predictivo)$',
                        message="El tipo debe ser preventivo, correctivo o predictivo."
                    )
                ]
            },

            'descripcion': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    "required": "La descripción es obligatoria.",
                    "blank": "La descripción no puede estar vacía.",
                    "null": "La descripción no puede ser nula."
                }
            },

            'fecha_mantenimiento': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    "required": "La fecha del mantenimiento es obligatoria.",
                    "null": "La fecha del mantenimiento no puede ser nula.",
                    "invalid": "Debe enviar una fecha válida con formato YYYY-MM-DD."
                }
            },

            'horas_realizadas': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    "required": "Las horas realizadas son obligatorias.",
                    "null": "Las horas realizadas no pueden ser nulas.",
                    "invalid": "Las horas realizadas deben ser un número entero válido."
                },
                'validators': [
                    MinValueValidator(0, message="Las horas realizadas no pueden ser negativas.")
                ]
            },

            'costo': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    "required": "El costo es obligatorio.",
                    "null": "El costo no puede ser nulo.",
                    "invalid": "Debe enviar un valor numérico válido para el costo."
                },
                'validators': [
                    MinValueValidator(0, message="El costo no puede ser negativo.")
                ]
            }
        }

    def validate_descripcion(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "La descripción debe tener mínimo 10 caracteres reales."
            )
        return value

    def validate_fecha_mantenimiento(self, value):
        if value > date.today():
            raise serializers.ValidationError("La fecha no puede ser futura.")
        return value

    def validate_costo(self, value):
        if value > 9_000_000:
            raise serializers.ValidationError(
                "El costo no puede superar los 9 millones."
            )
        return value

    def validate_horas_realizadas(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Las horas realizadas deben ser mayores a 0."
            )
        return value

    def validate(self, attrs):
        instancia = self.instance

        # Valores actuales SOLO si vienen en PATCH
        tipo = attrs.get('tipo_mantenimiento')
        programado = attrs.get('programado')
        maquina = attrs.get('maquina')
        horas = attrs.get('horas_realizadas')
        fecha = attrs.get('fecha_mantenimiento')
        costo = attrs.get('costo')

        # Si es PATCH, completar SOLO para reglas que dependen de varios campos
        if instancia:
            tipo = tipo if 'tipo_mantenimiento' in attrs else instancia.tipo_mantenimiento
            programado = programado if 'programado' in attrs else instancia.programado
            maquina = maquina if 'maquina' in attrs else instancia.maquina

        # ================================
        # 1. REGLAS DE TIPO / PROGRAMADO
        # ================================

        if 'tipo_mantenimiento' in attrs or 'programado' in attrs:
            if tipo != "correctivo" and programado is None:
                raise serializers.ValidationError(
                    "El mantenimiento solo puede omitir un mantenimiento programado si es de tipo correctivo."
                )

            if tipo == "correctivo" and programado is not None:
                raise serializers.ValidationError(
                    "Un mantenimiento correctivo no puede estar asociado a un mantenimiento programado."
                )

            if tipo == "predictivo" and programado is None:
                raise serializers.ValidationError(
                    "Un mantenimiento predictivo debe estar asociado a un mantenimiento programado."
                )

            if tipo == "preventivo" and programado:
                if programado.maquina.id_maquina != maquina.id_maquina:
                    raise serializers.ValidationError(
                        "El mantenimiento programado no corresponde a la misma máquina."
                    )

        # ==========================================
        # 2. HORAS REALIZADAS (SOLO SI VIENEN)
        # ==========================================

        if 'horas_realizadas' in attrs:
            if hasattr(maquina, 'horas_totales'):
                if horas < maquina.horas_totales:
                    raise serializers.ValidationError({
                        "horas_realizadas": (
                            f"Las horas realizadas ({horas}) no pueden ser menores "
                            f"a las horas totales actuales de la máquina ({maquina.horas_totales})."
                        )
                    })

            ultimo_mant = (
                Mantenimiento.objects
                .filter(maquina=maquina)
                .exclude(pk=getattr(instancia, 'pk', None))
                .order_by('-fecha_mantenimiento', '-id_mantenimiento')
                .first()
            )

            if ultimo_mant and horas < ultimo_mant.horas_realizadas:
                raise serializers.ValidationError({
                    "horas_realizadas": (
                        f"Las horas realizadas ({horas}) no pueden ser menores "
                        f"a las del último mantenimiento ({ultimo_mant.horas_realizadas})."
                    )
                })

        # ==========================================
        # 3. REGLAS ESPECIALES
        # ==========================================

        if tipo == "preventivo" and 'fecha_mantenimiento' in attrs:
            dif_anios = date.today().year - fecha.year
            if dif_anios > 10:
                raise serializers.ValidationError(
                    "Un mantenimiento preventivo no puede tener más de 10 años de antigüedad."
                )

        if tipo == "correctivo" and 'costo' in attrs and costo == 0:
            raise serializers.ValidationError(
                "Un mantenimiento correctivo debe tener un costo mayor a 0."
            )

        return attrs