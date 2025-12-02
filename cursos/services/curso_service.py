from rest_framework.exceptions import ValidationError

from cursos.repositories.curso_repository import CursoRepository
from cursos.serializers.curso_serializer import CursoSerializer
from cursos.services.curso_service_interface import ICursoService


class CursoService(ICursoService):
    """
    Servicio de lógica de negocio para la gestión de Cursos.
    Coordina validaciones (serializer) y persistencia (repository),
    aplicando reglas de negocio y retornando datos serializados.
    """

    # ---------------------------------------------------------
    # CREAR
    # ---------------------------------------------------------
    def crear_curso(self, data: dict):
        """
        Crea un curso:
        - Valida datos con el serializer
        - Aplica reglas de negocio (si las hubiera)
        - Guarda el curso mediante el repository
        - Retorna el curso serializado
        """
        serializer = CursoSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        curso = CursoRepository.create(**serializer.validated_data)
        return CursoSerializer(curso).data

    # ---------------------------------------------------------
    # LISTAR
    # ---------------------------------------------------------
    def listar_cursos(self):
        """Retorna todos los cursos registrados."""
        return CursoRepository.get_all()

    # ---------------------------------------------------------
    # OBTENER
    # ---------------------------------------------------------
    def obtener_curso(self, **kwargs):
        """
        Obtiene un curso por cualquier campo.
        Ejemplos:
            obtener_curso(id_curso=1)
            obtener_curso(usuario_id=5)
        Retorna None si no existe.
        """
        return CursoRepository.get_by_id(**kwargs)

    # ---------------------------------------------------------
    # OBTENER POR USUARIO
    # ---------------------------------------------------------
    def obtener_cursos_por_usuario(self, id_usuario: int):
        """
        Obtiene todos los cursos asociados a un usuario.
        Ejemplo:
            obtener_cursos_por_usuario(10)
        """
        return CursoRepository.get_by_usuario(id_usuario)

    # ---------------------------------------------------------
    # ACTUALIZAR (PUT o PATCH)
    # ---------------------------------------------------------
    def actualizar_curso(self, id_curso: int, data: dict, parcial: bool = True):
        """
        Actualiza un curso:
        - `parcial=True` → actualización tipo PATCH
        - `parcial=False` → actualización tipo PUT
        - Valida los datos con el serializer (parcial o completo)
        - Usa serializer con instancia para un update profesional
        - Retorna los datos actualizados serializados
        """
        curso = CursoRepository.get_by_id(id_curso=id_curso)

        if not curso:
            raise ValidationError({
                "id_curso": "No se encontró el curso a actualizar."
            })

        serializer = CursoSerializer(
            instance=curso,
            data=data,
            partial=parcial
        )
        serializer.is_valid(raise_exception=True)

        curso_actualizado = CursoRepository.update(
            id_curso=id_curso,
            **serializer.validated_data
        )

        return CursoSerializer(curso_actualizado).data

    # ---------------------------------------------------------
    # ELIMINAR
    # ---------------------------------------------------------
    def eliminar_curso(self, id_curso: int):
        """
        Elimina un curso por su ID.
        - Verifica existencia
        - Lanza error si no existe
        - Retorna True al eliminar correctamente
        """
        eliminado = CursoRepository.delete(id_curso)

        if not eliminado:
            raise ValidationError({
                "id_curso": "No se encontró el curso a eliminar."
            })

        return True
