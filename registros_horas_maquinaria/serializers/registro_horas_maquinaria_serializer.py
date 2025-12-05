from datetime import date

from django.core.validators import RegexValidator, MinValueValidator
from rest_framework import serializers

from proyecto_maquinaria.models.proyecto_maquinaria import ProyectoMaquinaria
from registros_horas_maquinaria.models.registro_horas_maquinaria import RegistroHorasMaquinaria

class RegistroHorasMaquinariaSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegistroHorasMaquinaria
        fields = [
            "id_registro",
            "maquina",
            "proyecto",
            "usuario",
            "fecha",
            "horas_trabajadas",
            "observaciones",
            "foto_planilla",
            "foto_horometro_inicial",
            "foto_horometro_final",
            "created_at",
            "updated_at"
        ]

        read_only_fields = ("id_registro", "created_at", "updated_at")

        extra_kwargs = {
            "maquina": {
                "required": True,
                "allow_null": False,
                "error_messages": {
                    "required": "La máquina es obligatoria.",
                    "null": "La máquina no puede ser nula."
                }
            },

            "fecha": {
                "required": True,
                "allow_null": False,
                "error_messages": {
                    "required": "La fecha es obligatoria.",
                    "null": "La fecha no puede ser nula.",
                    "invalid": "La fecha debe tener el formato YYYY-MM-DD."
                }
            },

            "horas_trabajadas": {
                "required": True,
                "allow_null": False,
                "error_messages": {
                    "required": "Las horas trabajadas son obligatorias.",
                    "null": "Las horas trabajadas no pueden ser nulas.",
                    "invalid": "Debe ingresar un número válido de horas."
                },
                "validators": [
                    MinValueValidator(
                        0,
                        message="Las horas trabajadas no pueden ser negativas."
                    )
                ]
            },

            "proyecto": {
                "required": False,
                "allow_null": True,
                "error_messages": {
                    "null": "El proyecto puede omitirse, pero si se envía no debe ser nulo explícitamente."
                }
            },

            "observaciones": {
                "required": False,
                "allow_blank": True,
                "validators": [
                    RegexValidator(
                        regex=r'^.{0,2000}$',
                        message="Las observaciones pueden tener máximo 2000 caracteres."
                    )
                ]
            }
        }

    def validate_fecha(self, value):
        """La fecha no puede ser futura."""
        if value > date.today():
            raise serializers.ValidationError("La fecha no puede ser futura.")
        return value

    def validate_horas_trabajadas(self, value):
        """Las horas registradas deben ser positivas."""
        if value <= 0:
            raise serializers.ValidationError(
                "Las horas trabajadas deben ser mayores a 0."
            )
        return value


    def validate(self, attrs):
        maquina = attrs.get("maquina") or getattr(self.instance, "maquina", None)
        fecha = attrs.get("fecha") or getattr(self.instance, "fecha", None)
        horas = attrs.get("horas_trabajadas") or getattr(self.instance, "horas_trabajadas", None)
        proyecto = attrs.get("proyecto") or getattr(self.instance, "proyecto", None)

        # ================================================================
        # 1. La máquina NO puede estar fuera de servicio
        # ================================================================
        if maquina.estado == "fuera de servicio":
            raise serializers.ValidationError(
                f"La máquina #{maquina.id_maquina} está fuera de servicio; no se pueden registrar horas."
            )

        # ================================================================
        # 2. Evitar duplicar registro en misma fecha por máquina
        # ================================================================
        qs = RegistroHorasMaquinaria.objects.filter(
            maquina=maquina,
            fecha=fecha
        )

        # Excluir el registro actual en caso de UPDATE
        if self.instance:
            qs = qs.exclude(id_registro=self.instance.id_registro)

        if qs.exists():
            raise serializers.ValidationError(
                f"Ya existe un registro para la máquina #{maquina.id_maquina} en la fecha {fecha}."
            )

        # ================================================================
        # 3. Validaciones cuando viene un proyecto
        # ================================================================
        if proyecto:
            # Verificar relación Proyecto - Maquinaria
            rel = ProyectoMaquinaria.objects.filter(
                proyecto=proyecto,
                maquina=maquina
            ).first()

            if not rel:
                raise serializers.ValidationError(
                    "La máquina no está asignada a este proyecto."
                )

            # Proyecto finalizado → no se permiten registros
            if rel.finalizado:
                raise serializers.ValidationError(
                    "Este proyecto ya fue finalizado; no se pueden registrar más horas."
                )

            # Validar que NO se excedan las horas pactadas
            if rel.horas_acumuladas + horas > rel.horas_totales:
                raise serializers.ValidationError(
                    f"Las horas registradas ({horas}) exceden el límite permitido para este "
                    f"proyecto ({rel.horas_totales} h). Horas acumuladas actuales: "
                    f"{rel.horas_acumuladas}."
                )

        return attrs