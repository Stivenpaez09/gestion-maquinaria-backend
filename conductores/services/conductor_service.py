from rest_framework.exceptions import ValidationError
from conductores.repositories.conductor_respository import ConductorRepository
from conductores.serializers.conductor_serializer import ConductorSerializer
from conductores.services.conductor_service_interface import IConductorService


class ConductorService(IConductorService):
    """
    Servicio de lógica de negocio para la gestión de Conductores.
    Coordina validaciones (serializer) y persistencia (repository),
    aplicando reglas de negocio como evitar duplicados por usuario.
    """

    # ---------------------------------------------------------
    # CREAR
    # ---------------------------------------------------------
    def crear_conductor(self, data: dict):
        """
        Crea un conductor:
        - Valida los datos con el serializer
        - Verifica regla de negocio: un usuario solo puede tener un conductor
        - Guarda el registro vía repository
        - Retorna datos serializados
        """
        serializer = ConductorSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        usuario = serializer.validated_data.get("usuario")

        # Regla de negocio: evitar duplicado por usuario
        if usuario and ConductorRepository.get_by_usuario(usuario.id_usuario).exists():
            raise ValidationError({
                "usuario": "Este usuario ya tiene un registro como conductor."
            })

        # Regla: el cargo debe ser 'conductor'
        if not usuario.cargo or usuario.cargo.lower() != "conductor":
            raise ValidationError({
                "usuario": "Este usuario no tiene el cargo de conductor."
            })

        conductor = ConductorRepository.create(**serializer.validated_data)
        return ConductorSerializer(conductor).data

    # ---------------------------------------------------------
    # LISTAR
    # ---------------------------------------------------------
    def listar_conductores(self):
        """Retorna todos los conductores registrados."""
        return ConductorRepository.get_all()

    # ---------------------------------------------------------
    # OBTENER
    # ---------------------------------------------------------
    def obtener_conductor(self, **kwargs):
        """
        Obtiene un conductor por cualquier campo.
        Ejemplo:
            obtener_conductor(id_conductor=1)
            obtener_conductor(usuario_id=5)
        """
        return ConductorRepository.get_by_id(**kwargs)

    # ---------------------------------------------------------
    # ACTUALIZAR (PUT o PATCH)
    # ---------------------------------------------------------
    def actualizar_conductor(self, id_conductor: int, data: dict, parcial: bool = True):
        """
        Actualiza un conductor:
        - `parcial=True` → actualización tipo PATCH
        - `parcial=False` → actualización tipo PUT
        - Valida datos con serializer (parcial o completo)
        - Si cambia el usuario, se verifica regla de negocio (no duplicar)
        - Retorna datos actualizados serializados
        """
        conductor = ConductorRepository.get_by_id(id_conductor=id_conductor)

        if not conductor:
            raise ValidationError({
                "id_conductor": "No se encontró el conductor a actualizar."
            })

        # Serializer con instancia → UPDATE profesional
        serializer = ConductorSerializer(
            instance=conductor,
            data=data,
            partial=parcial
        )
        serializer.is_valid(raise_exception=True)

        usuario = serializer.validated_data.get("usuario")

        # Regla de negocio: evitar duplicado por usuario si se cambia
        if usuario:
            otros = ConductorRepository.get_by_usuario(usuario.id).exclude(id_conductor=id_conductor)
            if otros.exists():
                raise ValidationError({
                    "usuario": "Este usuario ya está registrado como conductor."
                })

        conductor_actualizado = ConductorRepository.update(
            id_conductor=id_conductor,
            **serializer.validated_data
        )

        return ConductorSerializer(conductor_actualizado).data

    # ---------------------------------------------------------
    # ELIMINAR
    # ---------------------------------------------------------
    def eliminar_conductor(self, id_conductor: int):
        """
        Elimina un conductor por su ID.
        - Verifica existencia
        - Lanza error si no existe
        - Retorna True al eliminar correctamente
        """
        eliminado = ConductorRepository.delete(id_conductor)

        if not eliminado:
            raise ValidationError({
                "id_conductor": "No se encontró el conductor a eliminar."
            })

        return True
