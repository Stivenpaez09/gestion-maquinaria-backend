from django.core.validators import RegexValidator
from rest_framework import serializers

from alarmas.models.alarma import Alarma


class AlarmaSerializer(serializers.ModelSerializer):
    """
    Serializer profesional para la gestión de alarmas.
    Incluye validaciones robustas para garantizar integridad,
    coherencia semántica y evitar duplicados innecesarios.
    """

    class Meta:
        model = Alarma
        fields = [
            'id_alarma',
            'maquina',
            'descripcion',
            'tipo',
            'nivel',
            'fecha_registro',
            'vista',
            'created_at',
            'updated_at'
        ]

        read_only_fields = (
            'id_alarma',
            'fecha_registro',
            'created_at',
            'updated_at'
        )

        extra_kwargs = {
            'maquina': {'required': True},
            'descripcion': {
                'required': False,
                'allow_null': True,
                'allow_blank': True
            },
            'tipo': {
                'required': True,
                'validators': [
                    RegexValidator(
                        regex=r'^[a-zA-Z_ñÑáéíóúÁÉÍÓÚ]+$',
                        message="El tipo solo debe contener letras, sin espacios ni símbolos."
                    )
                ]
            },
            'nivel': {'required': False},
            'vista': {'required': False},
        }

    # ===============================
    # VALIDACIONES INDIVIDUALES
    # ===============================

    def validate_tipo(self, value):
        value = value.lower()
        tipos_validos = ['mantenimiento', 'proyecto', 'estado', 'sistema']

        if value not in tipos_validos:
            raise serializers.ValidationError(
                f"El tipo debe ser uno de: {', '.join(tipos_validos)}."
            )
        return value

    def validate_descripcion(self, value):
        if value and len(value.strip()) < 5:
            raise serializers.ValidationError(
                "La descripción debe tener mínimo 5 caracteres reales."
            )
        return value

    # ===============================
    # VALIDACIÓN GENERAL (PATCH-FRIENDLY)
    # ===============================

    def validate(self, attrs):
        """
        Validaciones cruzadas:
        - Evitar alarmas duplicadas no vistas del mismo tipo para la misma máquina.
        - Protección mínima para coherencia de nivel.
        """

        instancia = self.instance  # Solo existe en UPDATE/PATCH

        # Cargar valores nuevos o existentes (para soportar PATCH)
        maquina = attrs.get('maquina', getattr(instancia, 'maquina', None))
        tipo = attrs.get('tipo', getattr(instancia, 'tipo', None))
        nivel = attrs.get('nivel', getattr(instancia, 'nivel', None))
        descripcion = attrs.get('descripcion', getattr(instancia, 'descripcion', None))

        # =====================================================
        # VALIDAR DUPLICADOS DE ALARMAS NO VISTAS (solo CREATE)
        # =====================================================
        if instancia is None:
            if Alarma.objects.filter(maquina=maquina, tipo=tipo, vista=False).exists():
                raise serializers.ValidationError(
                    f"Ya existe una alarma activa (no vista) de tipo '{tipo}' para esta máquina."
                )

        # =====================================================
        # REGLAS DE NEGOCIO PARA NIVELES
        # =====================================================
        if nivel == "crítica" and not descripcion:
            raise serializers.ValidationError(
                "Las alarmas críticas deben incluir una descripción obligatoria."
            )

        return attrs

