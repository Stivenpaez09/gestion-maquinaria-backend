import cloudinary.uploader
from typing import Optional

from django.core.files.uploadedfile import UploadedFile
from django.db import transaction
from rest_framework.exceptions import NotFound, ValidationError

from alarmas.services.alarma_service import AlarmaService
from maquinarias.services.maquinaria_service import MaquinariaService
from proyecto_maquinaria.models.proyecto_maquinaria import ProyectoMaquinaria
from proyecto_maquinaria.services.proyecto_maquinaria_service import ProyectoMaquinariaService
from registros_horas_maquinaria.repositories.registro_horas_maquinaria_repository import \
    RegistroHorasMaquinariaRepository
from registros_horas_maquinaria.serializers.registro_horas_maquinaria_serializer import \
    RegistroHorasMaquinariaSerializer
from registros_horas_maquinaria.services.registro_horas_maquinaria_service_interface import \
    IRegistroHorasMaquinariaService


class RegistroHorasMaquinariaService(IRegistroHorasMaquinariaService):
    """
    Servicio profesional para la gestión de Registros de Horas de Maquinaria.

    Responsabilidades:
    - Validación con serializer
    - Actualización de horas_totales (Maquinaria)
    - Actualización de horas_acumuladas (ProyectoMaquinaria)
    - Persistencia mediante repository
    """
    def __init__(self):
        """Inyección de dependencias de otros servicios."""
        self.maquinaria_service = MaquinariaService()
        self.proyecto_maquinaria_service = ProyectoMaquinariaService()
        self.alarma_service = AlarmaService()

    # ----------------------------------------------------------------------
    # UTILIDAD: Guardar foto físicamente
    # ----------------------------------------------------------------------
    def _guardar_foto(self, foto_file: Optional[UploadedFile]) -> Optional[str]:
        """
        Guarda la foto en registros/photos/
        Retorna la URL absoluta final que se almacenará en BD.
        """
        if not foto_file:
            return None

        try:
            resultado = cloudinary.uploader.upload(
                foto_file,
                folder="registros/photos",  # carpeta lógica en Cloudinary
                resource_type="image"  # forzamos imagen
            )
            return resultado.get("secure_url")

        except Exception as e:
            raise ValidationError({"foto": "Error al subir la imagen"})

    # ----------------------------------------------------------------------
    # Listar
    # ----------------------------------------------------------------------
    def listar_registros(self):
        """Retorna todos los registros de horas."""
        return RegistroHorasMaquinariaRepository.get_all()

    # ----------------------------------------------------------------------
    # Obtener uno
    # ----------------------------------------------------------------------
    def obtener_registro(self, id_registro: int):
        """
        Obtiene un registro por ID.
        Lanza NotFound si no existe.
        """
        registro = RegistroHorasMaquinariaRepository.get_by_id(id_registro=id_registro)

        if registro is None:
            raise NotFound(detail=f"El registro con ID {id_registro} no existe.")

        return registro

    # ----------------------------------------------------------------------
    # Crear registro
    # ----------------------------------------------------------------------
    @transaction.atomic
    def crear_registro(self, data: dict):
        """
        Crea un registro de horas.

        Pasos:
        1. Valida datos con serializer
        2. Suma horas:
            - A Maquinaria.horas_totales
            - A ProyectoMaquinaria.horas_acumuladas (si viene proyecto)
        3. Persiste el registro
        """
        data = data.copy()
        foto_planilla = data.pop("foto_planilla", None)
        foto_horometro_inicial = data.pop("foto_horometro_inicial", None)
        foto_horometro_final = data.pop("foto_horometro_final", None)

        fotos = {
            "foto_planilla": foto_planilla,
            "foto_horometro_inicial": foto_horometro_inicial,
            "foto_horometro_final": foto_horometro_final
        }

        for key, value in fotos.items():
            if isinstance(value, list):
                fotos[key] = value[0] if value else None

        foto_planilla = fotos["foto_planilla"]
        foto_horometro_inicial = fotos["foto_horometro_inicial"]
        foto_horometro_final = fotos["foto_horometro_final"]

        serializer = RegistroHorasMaquinariaSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        if foto_planilla:
            ruta_foto = self._guardar_foto(foto_planilla)
            serializer.validated_data["foto_planilla"] = ruta_foto

        if foto_horometro_inicial:
            ruta_foto = self._guardar_foto(foto_horometro_inicial)
            serializer.validated_data["foto_horometro_inicial"] = ruta_foto

        if foto_horometro_final:
            ruta_foto = self._guardar_foto(foto_horometro_final)
            serializer.validated_data["foto_horometro_final"] = ruta_foto

        maquina = serializer.validated_data["maquina"]
        horas = serializer.validated_data["horas_trabajadas"]
        proyecto = serializer.validated_data.get("proyecto")

        # --- Actualizar totales de Maquinaria ---
        maquinaria = self.maquinaria_service.sumar_horas_maquinaria(maquina, horas)

        # --- Actualizar acumuladas si está asignada a proyecto ---
        if proyecto:
            try:
                pm = ProyectoMaquinaria.objects.get(
                    maquina=maquina,
                    proyecto=proyecto
                )
                pm = self.proyecto_maquinaria_service.sumar_horas_acumuladas(pm, horas)
            except ProyectoMaquinaria.DoesNotExist:
                pass

        # --- Validar y generar alarma
        self.alarma_service.validar_y_generar_alarmas(maquina.id_maquina)
        # Guardar registro
        registro = RegistroHorasMaquinariaRepository.create(
            **serializer.validated_data
        )

        return RegistroHorasMaquinariaSerializer(registro).data

    # ----------------------------------------------------------------------
    # Actualizar registro
    # ----------------------------------------------------------------------
    def actualizar_registro(self, id_registro: int, data: dict):
        """
        Actualiza parcialmente un registro.

        NOTA:
        - No re-suma horas (solo en crear)
        - Es una edición del registro, no recalcula acumulados
        """
        registro = self.obtener_registro(id_registro)
        data = data.copy()
        foto_planilla = data.pop("foto_planilla", None)
        foto_horometro_inicial = data.pop("foto_horometro_inicial", None)
        foto_horometro_final = data.pop("foto_horometro_final", None)

        if isinstance(foto_planilla, list):
            foto_planilla = foto_planilla[0] if foto_planilla else None

        if isinstance(foto_horometro_inicial, list):
            foto_horometro_inicial = foto_horometro_inicial[0] if foto_horometro_inicial else None

        if isinstance(foto_horometro_final, list):
            foto_horometro_final = foto_horometro_final[0] if foto_horometro_final else None

        serializer = RegistroHorasMaquinariaSerializer(
            instance=registro,
            data=data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        if foto_planilla:
            ruta_foto = self._guardar_foto(foto_planilla)
            serializer.validated_data["foto_planilla"] = ruta_foto

        if foto_horometro_inicial:
            ruta_foto = self._guardar_foto(foto_horometro_inicial)
            serializer.validated_data["foto_horometro_inicial"] = ruta_foto

        if foto_horometro_final:
            ruta_foto = self._guardar_foto(foto_horometro_final)
            serializer.validated_data["foto_horometro_final"] = ruta_foto

        actualizado = RegistroHorasMaquinariaRepository.update(
            id_registro=id_registro,
            **serializer.validated_data
        )

        return RegistroHorasMaquinariaSerializer(actualizado).data

    # ----------------------------------------------------------------------
    # Eliminar registro
    # ----------------------------------------------------------------------
    def eliminar_registro(self, id_registro: int):
        """
        Elimina un registro de horas por ID.
        No resta horas a acumulados.
        """
        self.obtener_registro(id_registro)
        RegistroHorasMaquinariaRepository.delete(id_registro)
        return True

    # ----------------------------------------------------------------------
    # Filtros
    # ----------------------------------------------------------------------
    def obtener_por_maquina(self, id_maquina: int):
        return RegistroHorasMaquinariaRepository.get_by_maquina(id_maquina)

    def obtener_por_proyecto(self, id_proyecto: int):
        return RegistroHorasMaquinariaRepository.get_by_proyecto(id_proyecto)

    def obtener_por_fecha(self, fecha):
        return RegistroHorasMaquinariaRepository.get_by_fecha(fecha)

    def obtener_entre_fechas(self, fecha_inicio, fecha_fin):
        return RegistroHorasMaquinariaRepository.get_between_fechas(fecha_inicio, fecha_fin)