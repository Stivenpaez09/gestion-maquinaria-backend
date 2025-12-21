import cloudinary.uploader
from typing import Optional

from django.core.files.uploadedfile import UploadedFile
from rest_framework.exceptions import ValidationError, NotFound

from usuarios.repositories.usuario_repository import UsuarioRepository
from usuarios.serializers.usuario_serializer import UsuarioSerializer
from usuarios.services.usuario_service_interface import IUsuarioService


class UsuarioService(IUsuarioService):
    """
    Servicio profesional para la gestión de Usuarios.
    Centraliza la lógica de negocio:
    - Validación con serializer
    - Reglas de negocio
    - Manejo de archivos (foto)
    - Operaciones con el repository
    """

    # ----------------------------------------------------------------------
    # UTILIDAD: Guardar foto físicamente
    # ----------------------------------------------------------------------
    def _guardar_foto(self, foto_file: Optional[UploadedFile]) -> Optional[str]:
        """
        Guarda la foto en usuarios/files/fotos/
        Retorna la URL absoluta final que se almacenará en BD.
        """
        if not foto_file:
            return None

        try:
            resultado = cloudinary.uploader.upload(
                foto_file,
                folder="usuarios/photos",  # carpeta lógica en Cloudinary
                resource_type="image"  # forzamos imagen
            )
            return resultado.get("secure_url")

        except Exception as e:
            raise ValidationError({"foto": "Error al subir la imagen"})

    # ----------------------------------------------------------------------
    # Listar Usuarios
    # ----------------------------------------------------------------------
    def listar_usuarios(self):
        """Retorna todos los usuarios registrados."""
        return UsuarioRepository.get_all()

    # ----------------------------------------------------------------------
    # Obtener Usuario
    # ----------------------------------------------------------------------
    def obtener_usuario(self, id_usuario: int):
        """
        Obtiene un usuario por ID.
        Lanza NotFound si no existe.
        """
        usuario = UsuarioRepository.get_by_id(id_usuario=id_usuario)
        if usuario is None:
            raise NotFound(detail=f"El usuario con ID {id_usuario} no existe.")
        return usuario


    # ----------------------------------------------------------------------
    # Crear Usuario
    # ----------------------------------------------------------------------
    def crear_usuario(self, data: dict):
        """
        Crea un nuevo usuario.
        Pasos:
        1. Extrae la foto del request (si existe)
        2. Valida datos con serializer
        3. Verifica email único
        4. Guarda físicamente la foto
        5. Persiste usando el repository
        """
        data = data.copy()
        foto_file = data.pop("foto", None)
        # ----- Normalización universal (soporta archivo único o array) -----
        if isinstance(foto_file, list):
            foto_file = foto_file[0] if foto_file else None

        serializer = UsuarioSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")

        # Validación: evitar correos duplicados
        if email and UsuarioRepository.get_by_email(email=email):
            raise ValidationError({"email": "Este correo ya está registrado."})

        # Si viene una foto → guardarla
        if foto_file:
            ruta_foto = self._guardar_foto(foto_file)
            serializer.validated_data["foto"] = ruta_foto

        usuario = UsuarioRepository.create(**serializer.validated_data)
        return usuario

    # ----------------------------------------------------------------------
    # Actualizar Usuario
    # ----------------------------------------------------------------------
    def actualizar_usuario(self, id_usuario: int, data: dict):
        """
        Actualiza un usuario existente.
        Pasos:
        1. Extrae foto si viene
        2. Valida datos
        3. Verifica email único
        4. Guarda nueva foto (opcional)
        5. Actualiza con repository
        """
        usuario = self.obtener_usuario(id_usuario)

        data = data.copy()
        foto_file = data.pop("foto", None)
        # ----- Normalización universal (soporta archivo único o array) -----
        if isinstance(foto_file, list):
            foto_file = foto_file[0] if foto_file else None

        serializer = UsuarioSerializer(usuario, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        new_email = serializer.validated_data.get("email")

        # Regla: evitar email duplicado
        if new_email:
            existing = UsuarioRepository.get_by_email(email=new_email)
            if existing and existing.id_usuario != usuario.id_usuario:
                raise ValidationError({
                    "email": "Este correo ya está registrado por otro usuario."
                })

        # ¿Se sube una nueva foto?
        if foto_file:
            nueva_ruta = self._guardar_foto(foto_file)
            serializer.validated_data["foto"] = nueva_ruta

        usuario_actualizado = UsuarioRepository.update(
            usuario, **serializer.validated_data
        )
        return usuario_actualizado

    # ----------------------------------------------------------------------
    # Eliminar Usuario
    # ----------------------------------------------------------------------
    def eliminar_usuario(self, id_usuario: int):
        """
        Elimina un usuario por su ID.
        Retorna True si se elimina correctamente.
        """
        usuario = self.obtener_usuario(id_usuario)
        UsuarioRepository.delete(usuario)
        return True