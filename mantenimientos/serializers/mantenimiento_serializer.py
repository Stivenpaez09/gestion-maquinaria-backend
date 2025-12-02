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

        # Cargar valores nuevos o existentes (PATCH seguro)
        tipo = attrs.get('tipo_mantenimiento', getattr(instancia, 'tipo_mantenimiento', None))
        programado = attrs.get('programado', getattr(instancia, 'programado', None))
        maquina = attrs.get('maquina', getattr(instancia, 'maquina', None))
        horas = attrs.get('horas_realizadas', getattr(instancia, 'horas_realizadas', None))
        fecha = attrs.get('fecha_mantenimiento', getattr(instancia, 'fecha_mantenimiento', None))
        costo = attrs.get('costo', getattr(instancia, 'costo', None))

        # ================================
        # 1. REGLA: tipos de mantenimiento
        # ================================
        # Solo se omite si el mantenimiento es correctivo
        if tipo != "correctivo" and programado is None:
            raise serializers.ValidationError(
                "El mantenimiento solo puede omitir un mantenimiento programado si es de tipo correctivo."
            )

        # Correctivo → NO debe tener mantenimiento_programado
        if tipo == "correctivo" and programado is not None:
            raise serializers.ValidationError(
                "Un mantenimiento correctivo no puede estar asociado a un mantenimiento programado."
            )

        # Predictivo → DEBE tener mantenimiento_programado
        if tipo == "predictivo" and programado is None:
            raise serializers.ValidationError(
                "Un mantenimiento predictivo debe estar asociado a un mantenimiento programado."
            )

        # Preventivo → programado es opcional
        if tipo == "preventivo" and programado:
            # Validar que pertenezcan a la misma máquina
            if programado.maquina.id_maquina != maquina.id_maquina:
                raise serializers.ValidationError(
                    "El mantenimiento programado no corresponde a la misma máquina."
                )

        # ==========================================
        # 2. Validar coherencia entre mantenimiento y mantenimiento_programado
        # ==========================================

        if programado:
            # 1. Tipo del programado debe coincidir
            if tipo in ["preventivo", "predictivo"]:
                if programado.tipo != tipo:
                    raise serializers.ValidationError(
                        f"El mantenimiento programado debe ser de tipo '{tipo}'."
                    )

            # 2. Máquinas deben coincidir sí o sí
            if programado.maquina.id_maquina != maquina.id_maquina:
                raise serializers.ValidationError(
                    "La máquina del mantenimiento y la del mantenimiento programado deben ser la misma.")

        # ==========================================
        # 3. Validación horas_realizadas vs. la máquina
        # ==========================================

        # (a) No puede ser menor a las horas_totales de la máquina
        if hasattr(maquina, 'horas_totales'):
            if horas < maquina.horas_totales:
                raise serializers.ValidationError(
                    f"Las horas realizadas ({horas}) no pueden ser menores a las horas totales actuales de la máquina ({maquina.horas_totales})."
                )

        # (b) No puede ser menor al último mantenimiento
        ultimo_mant = (
            Mantenimiento.objects
            .filter(maquina=maquina)
            .order_by('-fecha_mantenimiento', '-id_mantenimiento')
            .first()
        )

        if ultimo_mant and horas < ultimo_mant.horas_realizadas:
            raise serializers.ValidationError(
                f"Las horas realizadas ({horas}) no pueden ser menores a las del último mantenimiento ({ultimo_mant.horas_realizadas})."
            )

        # ==========================================
        # 3. Reglas de negocio especiales
        # ==========================================

        # Preventivo muy antiguo
        if tipo == "preventivo" and fecha:
            dif_anios = date.today().year - fecha.year
            if dif_anios > 10:
                raise serializers.ValidationError(
                    "Un mantenimiento preventivo no puede tener más de 10 años de antigüedad."
                )

        # Correctivo NO puede tener costo = 0
        if tipo == "correctivo" and attrs.get('costo') == 0:
            raise serializers.ValidationError(
                "Un mantenimiento correctivo debe tener un costo mayor a 0."
            )

        return attrs