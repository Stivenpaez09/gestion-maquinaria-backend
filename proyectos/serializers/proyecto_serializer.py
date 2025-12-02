from datetime import date

from django.core.validators import RegexValidator
from rest_framework import serializers

from proyectos.models.proyecto import Proyecto


class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = [
            'id_proyecto',
            'nombre_proyecto',
            'empresa',
            'descripcion',
            'fecha_inicio',
            'fecha_fin',
            'created_at',
            'updated_at'
        ]

        read_only_fields = ('id_proyecto', 'created_at', 'updated_at')

        extra_kwargs = {
            'empresa': {
                'required': False,
                'allow_null': True,
                'error_messages': {
                    'invalid': "ID de empresa inválido."
                }
            },
            'nombre_proyecto': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': "El nombre del proyecto es obligatorio.",
                    'blank': "El nombre del proyecto no puede estar vacío.",
                    'null': "El nombre del proyecto no puede ser nulo.",
                    'invalid': "Formato inválido para el nombre del proyecto."
                },
                'validators': [
                    RegexValidator(
                        regex=r'^.{3,150}$',
                        message="El nombre del proyecto debe tener entre 3 y 150 caracteres."
                    )
                ]
            },

            'descripcion': {
                'required': False,
                'allow_blank': True,
                'allow_null': True,
                'error_messages': {
                    'invalid': "La descripción enviada no es válida."
                },
                'validators': [
                    RegexValidator(
                        regex=r'^.{0,5000}$',
                        message="La descripción no puede exceder 5000 caracteres."
                    )
                ]
            },

            'fecha_inicio': {
                'required': False,
                'allow_null': True,
                'error_messages': {
                    'invalid': "La fecha de inicio debe tener formato YYYY-MM-DD."
                }
            },

            'fecha_fin': {
                'required': False,
                'allow_null': True,
                'error_messages': {
                    'invalid': "La fecha de fin debe tener formato YYYY-MM-DD."
                }
            }
        }

    def validate_nombre_proyecto(self, value):
        if Proyecto.objects.filter(nombre_proyecto__iexact=value).exists():
            raise serializers.ValidationError("Ya existe un proyecto con este nombre.")
        return value

    def validate(self, data):
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                raise serializers.ValidationError(
                    {"fecha_fin": "La fecha de fin no puede ser menor a la fecha de inicio."}
                )

        hoy = date.today()
        if fecha_inicio and fecha_inicio > hoy:
            raise serializers.ValidationError(
                {"fecha_inicio": "La fecha de inicio no puede ser en el futuro."}
            )

        return data