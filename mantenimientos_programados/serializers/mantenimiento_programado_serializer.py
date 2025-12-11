from rest_framework import serializers

from mantenimientos_programados.models.mantenimiento_programado import MantenimientoProgramado
from mantenimientos_programados.repositories.mantenimiento_programado_repository import \
    MantenimientoProgramadoRepository
from maquinarias.models.maquinaria import Maquinaria


class MantenimientoProgramadoSerializer(serializers.ModelSerializer):
    """
    Serializer profesional para la gestión de mantenimientos programados.
    Incluye validaciones de negocio, consistencia de datos y formatos adecuados.
    """

    tipo = serializers.ChoiceField(
        choices=[
            ('preventivo', 'Preventivo'),
            ('predictivo', 'Predictivo')
        ],
        error_messages={
            "invalid_choice": "El tipo debe ser preventivo o predictivo.",
            "null": "El campo tipo no puede ser nulo.",
            "blank": "El campo tipo no puede estar vacío.",
            "required": "El campo tipo es obligatorio."
        }
    )

    class Meta:
        model = MantenimientoProgramado
        fields = [
            'id_programado',
            'nombre',
            'maquina',
            'tipo',
            'intervalo_horas',
            'descripcion',
            'created_at',
            'updated_at'
        ]

        read_only_fields = ('id_programado', 'created_at', 'updated_at')

        extra_kwargs = {
            'maquina': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    "required": "La máquina es obligatoria.",
                    "null": "La máquina no puede ser nula."
                }
            },
            'nombre': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    "required": "El nombre del mantenimiento es obligatorio.",
                    "blank": "El nombre no puede estar vacío.",
                    "null": "El nombre no puede ser nulo."
                }
            },
            'intervalo_horas': {
                'required': True
            },
            'descripcion': {
                'required': False,
                'allow_blank': True
            }
        }

    def validate_nombre(self, value):
        """Validar que no sea solo espacios."""
        if len(value.strip()) == 0:
            raise serializers.ValidationError("El nombre no puede contener solo espacios.")
        return value

    def validate_maquina(self, value):
        """Validar que la maquinaria exista y esté activa."""
        if not Maquinaria.objects.filter(id_maquina=value.id_maquina).exists():
            raise serializers.ValidationError("La maquinaria especificada no existe.")

        return value

    def validate_tipo(self, value):
        """Validar que no sea solo espacios."""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El tipo de mantenimiento no puede contener solo espacios.")
        return value

    def validate_intervalo_horas(self, value):
        """Validar que el intervalo sea positivo y razonable."""
        if value <= 0:
            raise serializers.ValidationError("El intervalo de horas debe ser mayor que cero.")

        # límite razonable: 100,000 horas
        if value > 100000:
            raise serializers.ValidationError("El intervalo de horas no puede exceder 100,000 horas.")

        return value

    def validate_descripcion(self, value):
        """Validar que no sea solo espacios (si viene)."""
        if value and len(value.strip()) == 0:
            raise serializers.ValidationError("La descripción no puede contener solo espacios.")
        return value

    # ----------------------------
    # Validaciones globales
    # ----------------------------

    def validate(self, attrs):
        """
        Validaciones cruzadas:
        - Evitar duplicado del nombre por máquina.
        """

        maquina = attrs.get("maquina") or getattr(self.instance, "maquina", None)
        nombre = attrs.get("nombre") or getattr(self.instance, "nombre", None)

        # ID a excluir si es actualización
        exclude_id = self.instance.id_programado if self.instance else None

        if MantenimientoProgramadoRepository.exists_by_maquina_y_nombre(
            id_maquina=maquina.id_maquina,
            nombre=nombre,
            exclude_id=exclude_id
        ):
            raise serializers.ValidationError(
                f"Ya existe un mantenimiento con el nombre '{nombre}' para esta maquinaria."
            )

        return attrs