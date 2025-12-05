import os
import uuid
from typing import Optional

from django.core.files.uploadedfile import UploadedFile
from rest_framework.exceptions import NotFound, ValidationError

from mantenimientos.repositories.mantenimiento_repository import MantenimientoRepository
from mantenimientos.serializers.mantenimiento_serializer import MantenimientoSerializer
from mantenimientos.services.mantenimiento_service_interface import IMantenimientoService
from servimacons import settings


class MantenimientoService(IMantenimientoService):
    """
    Servicio profesional para la gestión de Mantenimientos.
    Centraliza lógica de negocio:
    - Validación con serializer
    - Manejo de archivos (evidencia)
    - Reglas de negocio
    - Persistencia mediante repository
    """

    # ----------------------------------------------------------------------
    # UTILIDAD: Guardar archivo físicamente
    # ----------------------------------------------------------------------
    def _guardar_foto(self, foto_file: Optional[UploadedFile]) -> Optional[str]:
        """
        Guarda la foto del mantenimiento en:
        mantenimientos/photos/

        Retorna la URL absoluta final que se almacena en la BD.
        """
        if not foto_file:
            return None

        # Carpeta dentro de MEDIA_ROOT
        carpeta_relativa = "mantenimientos/photos"
        carpeta_absoluta = os.path.join(settings.MEDIA_ROOT, carpeta_relativa)

        # Crear carpeta si no existe
        os.makedirs(carpeta_absoluta, exist_ok=True)

        # Generar nombre único
        extension = foto_file.name.split('.')[-1]
        filename = f"{uuid.uuid4()}.{extension}"

        # Ruta física
        ruta_fisica = os.path.join(carpeta_absoluta, filename)

        # Guardado del archivo en disco
        with open(ruta_fisica, "wb+") as destino:
            for chunk in foto_file.chunks():
                destino.write(chunk)

        # Construir URL accesible públicamente
        url_relativa = f"{settings.MEDIA_URL}{carpeta_relativa}/{filename}"

        return url_relativa

    # ----------------------------------------------------------------------
    # Listar
    # ----------------------------------------------------------------------
    def listar_mantenimientos(self):
        """Retorna todos los mantenimientos registrados."""
        return MantenimientoRepository.get_all()

    # ----------------------------------------------------------------------
    # Obtener uno
    # ----------------------------------------------------------------------
    def obtener_mantenimiento(self, id_mantenimiento: int):
        """
        Obtiene un mantenimiento por ID.
        Lanza NotFound si no existe.
        """
        mantenimiento = MantenimientoRepository.get_by_id(id_mantenimiento=id_mantenimiento)

        if mantenimiento is None:
            raise NotFound(detail=f"El mantenimiento con ID {id_mantenimiento} no existe.")

        return mantenimiento

    def obtener_mantenimientos_por_maquina(self, id_maquina: int):
        """Retorna mantenimientos filtrados por máquina."""
        return MantenimientoRepository.get_by_maquina(id_maquina)

    def obtener_mantenimientos_por_usuario(self, id_usuario: int):
        """Retorna mantenimientos filtrados por usuario."""
        return MantenimientoRepository.get_by_usuario(id_usuario)

    # ----------------------------------------------------------------------
    # Crear
    # ----------------------------------------------------------------------
    def crear_mantenimiento(self, data: dict):
        """
        Crea un nuevo mantenimiento.

        Pasos:
        1. Extrae foto si se envió
        2. Valida datos con serializer
        3. Guarda foto físicamente (opcional)
        4. Persiste mediante repository
        """
        print("se envia el elemento para que se cree el nuevo mantenimiento.")
        data = data.copy()
        foto_file = data.pop("foto", None)

        # ----- Normalización universal (soporta archivo único o array) -----
        if isinstance(foto_file, list):
            foto_file = foto_file[0] if foto_file else None

        serializer = MantenimientoSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        maquinaria = serializer.validated_data.get("maquina", None)

        # Guardar foto si viene en el request
        if foto_file:
            ruta_foto = self._guardar_foto(foto_file)
            serializer.validated_data["foto"] = ruta_foto

        from maquinarias.services.maquinaria_service import MaquinariaService
        maquinaria_service = MaquinariaService()
        maquinaria_service.actualizar_estado_maquinaria(id_maquina=maquinaria.id_maquina, estado="operativa")
        mantenimiento = MantenimientoRepository.create(
            **serializer.validated_data
        )

        return MantenimientoSerializer(mantenimiento).data

    # ----------------------------------------------------------------------
    # Actualizar
    # ----------------------------------------------------------------------
    def actualizar_mantenimiento(self, id_mantenimiento: int, data: dict):
        """
        Actualiza un mantenimiento existente.

        Pasos:
        1. Verifica existencia
        2. Extrae foto (si viene)
        3. Valida datos parcialmente
        4. Guarda nueva foto si se envía una
        5. Actualiza vía repository
        """
        mantenimiento = self.obtener_mantenimiento(id_mantenimiento=id_mantenimiento)

        if not mantenimiento:
            raise ValidationError({
                "id_mantenimiento": "No se encontró el mantenimiento a actualizar."
            })

        data = data.copy()
        foto_file = data.pop("foto", None)
        # ----- Normalización universal (soporta archivo único o array) -----
        if isinstance(foto_file, list):
            foto_file = foto_file[0] if foto_file else None

        serializer = MantenimientoSerializer(
            instance=mantenimiento,
            data=data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        # Si suben una nueva foto → guardarla
        if foto_file:
            nueva_ruta = self._guardar_foto(foto_file)
            serializer.validated_data["foto"] = nueva_ruta

        mantenimiento_actualizado = MantenimientoRepository.update(
            id_mantenimiento=id_mantenimiento,
            **serializer.validated_data
        )

        return MantenimientoSerializer(mantenimiento_actualizado).data

    # ----------------------------------------------------------------------
    # Eliminar
    # ----------------------------------------------------------------------
    def eliminar_mantenimiento(self, id_mantenimiento: int):
        """
        Elimina un mantenimiento por su ID.
        Lanza error si no existe.
        """
        mantenimiento = self.obtener_mantenimiento(id_mantenimiento)

        MantenimientoRepository.delete(id_mantenimiento)
        return True

    # ----------------------------------------------------------------------
    # OBTENER ÚLTIMO MANTENIMIENTO POR MÁQUINA
    # ----------------------------------------------------------------------
    def obtener_ultimo_mantenimiento_por_maquina(self, id_maquina: int):
        """
        Obtiene el último mantenimiento registrado para una máquina.
        Retorna None si no existe ningún mantenimiento.
        """
        mantenimientos = MantenimientoRepository.get_by_maquina(id_maquina)

        if not mantenimientos:
            return None

        # Ordenar por fecha descendente y retornar el primero (más reciente)
        return mantenimientos.order_by('-fecha_mantenimiento').first()

    # ----------------------------------------------------------------------
    # OBTENER ÚLTIMO MANTENIMIENTO POR MÁQUINA Y TIPO
    # ----------------------------------------------------------------------
    def obtener_ultimo_mantenimiento_por_maquina_y_tipo(self, id_maquina: int, tipo: str):
        """
        Obtiene el último mantenimiento de un tipo específico para una máquina.
        
        Ejemplo:
            obtener_ultimo_mantenimiento_por_maquina_y_tipo(5, 'preventivo')
        
        Retorna None si no existe.
        """
        return MantenimientoRepository.get_ultimo_por_maquina_y_tipo(id_maquina, tipo)

    # ----------------------------------------------------------------------
    # OBTENER ÚLTIMO MANTENIMIENTO POR MÁQUINA Y PROGRAMADO
    # -----------------------------------------------------------------
    def obtener_ultimo_mantenimiento_por_maquina_y_programado(self, id_maquina: int, id_programado: int):
        """
        Obtiene el último mantenimiento realizado a una máquina según un
        mantenimiento programado específico.
        """
        return MantenimientoRepository.get_ultimo_por_maquina_y_programado(
            id_maquina,
            id_programado
        )

