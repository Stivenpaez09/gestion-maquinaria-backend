from datetime import date

from django.core.validators import RegexValidator
from rest_framework import serializers

from cursos.models.curso import Curso


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = [
            'id_curso',
            'usuario',
            'nombre_curso',
            'institucion',
            'fecha_inicio',
            'fecha_fin',
            'created_at',
            'updated_at'
        ]

        read_only_fields = ('id_curso', 'created_at', 'updated_at')

        extra_kwargs = {
            'usuario': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    'required': "El usuario es obligatorio.",
                    'null': "El usuario no puede ser nulo.",
                    'invalid': "El usuario enviado no es válido."
                }
            },
            'nombre_curso': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': "El nombre del curso es obligatorio.",
                    'blank': "El nombre del curso no puede estar vacío.",
                    'null': "El nombre del curso no puede ser nulo.",
                    'invalid': "Formato inválido para el nombre del curso."
                },
                'validators': [
                    RegexValidator(
                        regex=r'^.{3,150}$',
                        message="El nombre del curso debe tener entre 3 y 150 caracteres."
                    )
                ]
            },
            'institucion': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': "La institución es obligatoria.",
                    'blank': "El nombre de la institución no puede estar vacío.",
                    'null': "La institución no puede ser nula.",
                    'invalid': "Formato inválido para el nombre de la institución."
                },
                'validators': [
                    RegexValidator(
                        regex=r'^.{3,150}$',
                        message="El nombre de la institución debe tener entre 3 y 150 caracteres."
                    )
                ]
            },
            'fecha_inicio': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    'required': "La fecha de inicio es obligatoria.",
                    'null': "La fecha de inicio no puede ser nula.",
                    'invalid': "La fecha de inicio debe tener formato YYYY-MM-DD."
                }
            },
            'fecha_fin': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    'required': "La fecha de fin es obligatoria.",
                    'null': "La fecha de fin no puede ser nula.",
                    'invalid': "La fecha de fin debe tener formato YYYY-MM-DD."
                }
            }
        }

    def validate_nombre_curso(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El nombre no puede tener solo espacios.")
        return value

    def validate_institucion(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El nombre de la institución no puede tener solo espacios.")
        return value

    def validate_fecha_inicio(self, value):
        today = date.today()

        if value > today:
            raise serializers.ValidationError("La fecha de inicio no puede ser futura.")

        return value

    def validate_fecha_fin(self, value):
        today = date.today()

        if value > today:
            raise serializers.ValidationError("La fecha de fin no puede ser futura.")

        return value


    def validate(self, attrs):
        fecha_inicio = attrs.get('fecha_inicio')
        fecha_fin = attrs.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            # Fecha fin no puede ser menor
            if fecha_fin < fecha_inicio:
                raise serializers.ValidationError(
                    "La fecha de fin no puede ser anterior a la fecha de inicio."
                )

            # Duración máxima de 10 años
            anios = fecha_fin.year - fecha_inicio.year
            if anios > 10:
                raise serializers.ValidationError(
                    "Un curso no puede durar más de 10 años."
                )

        return attrs
