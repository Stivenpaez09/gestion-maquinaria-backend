import os
import uuid
from typing import Optional

from django.core.files.uploadedfile import UploadedFile
from rest_framework.exceptions import NotFound

from hojas_vida.repositories.hoja_vida_repository import HojaVidaRepository
from hojas_vida.serializers.hoja_vida_serializer import HojaVidaSerializer
from hojas_vida.services.hoja_vida_service_interface import IHojaVidaService
from servimacons import settings


class HojaVidaService(IHojaVidaService):
    """
    Servicio profesional para la gestión de Hojas de Vida.
    Centraliza la lógica de negocio:
    - Validación con serializer
    - Reglas de negocio
    - Manejo de archivos físicos
    - Operaciones con el repository
    """

    # ----------------------------------------------------------------------
    # UTILIDAD: Guardar archivo físicamente
    # ----------------------------------------------------------------------
    def _guardar_archivo(self, archivo_file: Optional[UploadedFile]) -> Optional[str]:
        """
        Guarda el archivo en 'hojas_vida/files/'.
        Retorna la URL absoluta final o None.
        """
        if archivo_file is None:
            return None

        carpeta_relativa = "hojas_vida/files"
        carpeta_absoluta = os.path.join(settings.MEDIA_ROOT, carpeta_relativa)
        os.makedirs(carpeta_absoluta, exist_ok=True)

        extension = archivo_file.name.split('.')[-1]
        filename = f"{uuid.uuid4()}.{extension}"

        ruta_fisica = os.path.join(carpeta_absoluta, filename)

        with open(ruta_fisica, "wb+") as destino:
            for chunk in archivo_file.chunks():
                destino.write(chunk)

        url_final = f"{settings.MEDIA_URL}{carpeta_relativa}/{filename}"

        return url_final

    # ----------------------------------------------------------------------
    # Listar Hojas de Vida
    # ----------------------------------------------------------------------
    def listar_hojas_vida(self):
        """Retorna todas las hojas de vida registradas."""
        return HojaVidaRepository.get_all()

    # ----------------------------------------------------------------------
    # Obtener Hoja de Vida
    # ----------------------------------------------------------------------
    def obtener_hoja_vida(self, id_hoja: int):
        """
        Obtiene una hoja de vida por ID.
        Lanza NotFound si no existe.
        """
        hoja = HojaVidaRepository.get_by_id(id_hoja=id_hoja)
        if hoja is None:
            raise NotFound(detail=f"La hoja de vida con ID {id_hoja} no existe.")
        return hoja

    # ----------------------------------------------------------------------
    # Crear Hoja de Vida
    # ----------------------------------------------------------------------
    def crear_hoja_vida(self, data: dict):
        """
        Crea una nueva hoja de vida.
        Pasos:
        1. Extrae el archivo del request (si existe)
        2. Valida datos con serializer
        3. Guarda físicamente el archivo
        4. Persiste usando el repository
        """
        data = data.copy()
        archivo_file = data.pop("archivo", None)
        # ----- Normalización universal (soporta archivo único o array) -----
        if isinstance(archivo_file, list):
            archivo_file = archivo_file[0] if archivo_file else None

        serializer = HojaVidaSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Si viene un archivo → guardarlo
        if archivo_file:
            ruta_archivo = self._guardar_archivo(archivo_file)
            serializer.validated_data["archivo"] = ruta_archivo

        hoja = HojaVidaRepository.create(**serializer.validated_data)
        return hoja

    # ----------------------------------------------------------------------
    # Actualizar Hoja de Vida
    # ----------------------------------------------------------------------
    def actualizar_hoja_vida(self, id_hoja: int, data: dict):
        """
        Actualiza una hoja de vida existente.
        Pasos:
        1. Extrae archivo si viene
        2. Valida datos con serializer
        3. Guarda nueva versión del archivo (opcional)
        4. Actualiza con repository
        """
        hoja = self.obtener_hoja_vida(id_hoja)
        data = data.copy()
        archivo_file = data.pop("archivo", None)
        # ----- Normalización universal (soporta archivo único o array) -----
        if isinstance(archivo_file, list):
            archivo_file = archivo_file[0] if archivo_file else None

        serializer = HojaVidaSerializer(hoja, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        # ¿Se sube un nuevo archivo?
        if archivo_file:
            nueva_ruta = self._guardar_archivo(archivo_file)
            serializer.validated_data["archivo"] = nueva_ruta

        hoja_actualizada = HojaVidaRepository.update(
            hoja, **serializer.validated_data
        )
        return hoja_actualizada

    # ----------------------------------------------------------------------
    # Eliminar Hoja de Vida
    # ----------------------------------------------------------------------
    def eliminar_hoja_vida(self, id_hoja: int):
        """
        Elimina una hoja de vida por su ID.
        Retorna True si se elimina correctamente.
        """
        hoja = self.obtener_hoja_vida(id_hoja)
        HojaVidaRepository.delete(hoja)
        return True