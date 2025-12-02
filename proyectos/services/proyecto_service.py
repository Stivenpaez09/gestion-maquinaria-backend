from rest_framework.exceptions import ValidationError, NotFound

from proyectos.repositories.proyecto_repository import ProyectoRepository
from proyectos.serializers.proyecto_serializer import ProyectoSerializer
from proyectos.services.proyecto_service_interface import IProyectoService


class ProyectoService(IProyectoService):
    """
    Servicio profesional para la gestión de Proyectos.
    Encapsula toda la lógica de negocio:
    - Validación con serializer
    - Reglas de negocio
    - Persistencia con el repository
    """

    # ----------------------------------------------------------------------
    # Crear Proyecto
    # ----------------------------------------------------------------------
    def crear_proyecto(self, data: dict):
        """
        Crea un nuevo proyecto.
        Pasos:
        1. Valida los datos con el serializer.
        2. Aplica reglas de negocio.
        3. Persiste usando el repository.
        """
        serializer = ProyectoSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        nombre = serializer.validated_data.get("nombre_proyecto")

        # Regla de negocio: evitar nombre duplicado
        if nombre and ProyectoRepository.get_by_id(nombre_proyecto=nombre):
            raise ValidationError({
                "nombre_proyecto": "Ya existe un proyecto con este nombre."
            })

        proyecto = ProyectoRepository.create(**serializer.validated_data)
        return proyecto

    # ----------------------------------------------------------------------
    # Listar Proyectos
    # ----------------------------------------------------------------------
    def listar_proyectos(self):
        """Retorna todos los proyectos existentes."""
        return ProyectoRepository.get_all()

    # ----------------------------------------------------------------------
    # Obtener Proyecto
    # ----------------------------------------------------------------------
    def obtener_proyecto(self, **kwargs):
        """
        Obtiene un proyecto por cualquier campo.
        Ejemplo:
            obtener_proyecto(id_proyecto=1)
            obtener_proyecto(nombre_proyecto="Sistema X")
        """
        proyecto = ProyectoRepository.get_by_id(**kwargs)
        if proyecto is None:
            raise NotFound("El proyecto solicitado no existe.")
        return proyecto

    # ----------------------------------------------------------------------
    # Actualizar Proyecto
    # ----------------------------------------------------------------------
    def actualizar_proyecto(self, id_proyecto: int, data: dict):
        """
        Actualiza un proyecto existente.
        Pasos:
        1. Valida los datos.
        2. Aplica reglas de negocio.
        3. Actualiza usando el repository.
        """
        asignacion = self.obtener_proyecto(id_proyecto=id_proyecto)
        serializer = ProyectoSerializer(asignacion, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        proyecto_actualizado = ProyectoRepository.update(
            id_proyecto=id_proyecto,
            **serializer.validated_data
        )

        if proyecto_actualizado is None:
            raise NotFound("No se encontró el proyecto a actualizar.")

        return proyecto_actualizado

    # ----------------------------------------------------------------------
    # Eliminar Proyecto
    # ----------------------------------------------------------------------
    def eliminar_proyecto(self, id_proyecto: int):
        """
        Elimina un proyecto por ID.
        Retorna True si se eliminó correctamente.
        """
        proyecto = self.obtener_proyecto(id_proyecto=id_proyecto)
        eliminado = ProyectoRepository.delete(id_proyecto)

        if not eliminado:
            raise NotFound("No se encontró el proyecto a eliminar.")

        return True

    # ----------------------------------------------------------------------
    # Listar proyectos por empresa
    # ----------------------------------------------------------------------
    def listar_proyectos_por_empresa(self, id_empresa: int):
        """
        Retorna todos los proyectos asociados a una empresa específica.
        """
        proyectos = ProyectoRepository.get_by_empresa(id_empresa)

        return proyectos

