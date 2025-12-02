from datetime import date

from rest_framework import serializers
from proyecto_maquinaria.models.proyecto_maquinaria import ProyectoMaquinaria


class ProyectoMaquinariaSerializer(serializers.ModelSerializer):
    """
    Serializer profesional para ProyectoMaquinaria.
    Incluye validaciones sólidas y consistentes con el modelo actualizado.
    """

    class Meta:
        model = ProyectoMaquinaria
        fields = [
            'id_proyecto_maquinaria',
            'proyecto',
            'maquina',
            'fecha_asignacion',
            'horas_totales',
            'horas_acumuladas',
            'finalizado',
            'created_at',
            'updated_at'
        ]

        read_only_fields = (
            'id_proyecto_maquinaria',
            'fecha_asignacion',
            'created_at',
            'updated_at'
        )

        extra_kwargs = {
            'proyecto': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    'required': "Debe especificar el proyecto asociado.",
                    'null': "El proyecto no puede ser nulo."
                }
            },
            'maquina': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    'required': "Debe especificar la máquina asociada.",
                    'null': "La máquina no puede ser nula."
                }
            },
            'horas_totales': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    'required': "Debe indicar las horas totales pactadas.",
                    'null': "Las horas totales no pueden ser nulas."
                }
            },
            'horas_acumuladas': {
                'required': False,
                'allow_null': True,
                'error_messages': {
                    'null': "Las horas acumuladas no pueden ser nulas."
                }
            },
            'finalizado': {
                'required': False,
                'allow_null': True,
                'error_messages': {
                    'null': "El estado de finalización no puede ser nulo."
                }
            }
        }

    # ==============================
    # VALIDACIONES INDIVIDUALES
    # ==============================

    def validate_fecha_asignacion(self, value):
        """La fecha de asignación no puede ser futura."""
        if value > date.today():
            raise serializers.ValidationError(
                "La fecha de asignación no puede ser futura."
            )
        return value

    def validate_horas_totales(self, value):
        """Las horas totales no pueden ser negativas."""
        if value < 0:
            raise serializers.ValidationError("Las horas totales no pueden ser negativas.")
        return value

    def validate_horas_acumuladas(self, value):
        """Las horas acumuladas no pueden ser negativas."""
        if value < 0:
            raise serializers.ValidationError("Las horas acumuladas no pueden ser negativas.")
        return value

    # ==============================
    # VALIDACIÓN GENERAL
    # ==============================

    def validate(self, attrs):
        proyecto = attrs.get('proyecto')
        maquina = attrs.get('maquina')
        horas_totales = attrs.get('horas_totales')
        horas_acumuladas = attrs.get('horas_acumuladas', 0)

        # 1. Estado de la máquina
        if maquina and hasattr(maquina, 'estado') and maquina.estado != 'operativa':
            raise serializers.ValidationError(
                f"La máquina '{maquina.nombre_maquina}' no está operativa "
                f"(estado actual: {maquina.estado})."
            )

        # 2. Proyecto finalizado
        if proyecto and proyecto.fecha_fin and proyecto.fecha_fin < date.today():
            raise serializers.ValidationError(
                "No se puede asignar máquinas a un proyecto que ya ha finalizado."
            )

        # 3. Máquina ya asignada a otro proyecto activo
        conflicto = ProyectoMaquinaria.objects.filter(
            maquina=maquina,
            finalizado=False
        ).exclude(
            id_proyecto_maquinaria=self.instance.id_proyecto_maquinaria
            if self.instance else None
        ).first()

        if conflicto:
            raise serializers.ValidationError(
                f"La máquina '{maquina.nombre_maquina}' ya está asignada a otro proyecto "
                f"(Proyecto #{conflicto.proyecto.id_proyecto}) que no ha finalizado."
            )

        # 4. **Nueva validación** → No permitir duplicado proyecto + máquina
        if proyecto and maquina:
            duplicado = ProyectoMaquinaria.objects.filter(
                proyecto=proyecto,
                maquina=maquina
            )

            # excluir el mismo registro si es update
            if self.instance:
                duplicado = duplicado.exclude(
                    id_proyecto_maquinaria=self.instance.id_proyecto_maquinaria
                )

            if duplicado.exists():
                raise serializers.ValidationError(
                    f"La máquina '{maquina.nombre_maquina}' ya está asignada a este mismo proyecto. "
                    f"No se permite duplicar la asignación."
                )

        # 5. horas_acumuladas no puede superar horas_totales
        if horas_totales is not None and horas_acumuladas is not None:
            if horas_acumuladas > horas_totales:
                raise serializers.ValidationError(
                    "Las horas acumuladas no pueden superar las horas totales pactadas."
                )

        return attrs