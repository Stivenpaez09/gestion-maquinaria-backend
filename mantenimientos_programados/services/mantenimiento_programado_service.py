from rest_framework.exceptions import ValidationError

from mantenimientos_programados.repositories.mantenimiento_programado_repository import MantenimientoProgramadoRepository
from mantenimientos_programados.serializers.mantenimiento_programado_serializer import MantenimientoProgramadoSerializer
from mantenimientos_programados.services.mantenimiento_programado_service_interface import IMantenimientoProgramadoService
from maquinarias.repositories.maquinaria_repository import MaquinariaRepository

class MantenimientoProgramadoService(IMantenimientoProgramadoService):
    """
    Servicio de lógica de negocio para la gestión de Mantenimientos Programados.
    Coordina validaciones (serializer) y persistencia (repository),
    asegurando reglas de negocio como la existencia de la máquina asociada.
    """

    # ---------------------------------------------------------
    # CREAR
    # ---------------------------------------------------------
    def crear_mantenimiento_programado(self, data: dict):
        """
        Crea un mantenimiento programado:
        - Valida los datos con el serializer
        - Regla de negocio: la máquina debe existir
        - Guarda el registro mediante el repository
        - Retorna datos serializados
        """
        serializer = MantenimientoProgramadoSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        maquina = serializer.validated_data.get("maquina")

        # Regla de negocio: validar existencia de la máquina
        if not MaquinariaRepository.get_by(id_maquina=maquina.id_maquina):
            raise ValidationError({
                "maquina": "La máquina asociada no existe."
            })

        mantenimiento = MantenimientoProgramadoRepository.create(
            **serializer.validated_data
        )

        return MantenimientoProgramadoSerializer(mantenimiento).data

    # ---------------------------------------------------------
    # LISTAR
    # ---------------------------------------------------------
    def listar_mantenimientos_programados(self):
        """Retorna todos los mantenimientos programados registrados."""
        return MantenimientoProgramadoRepository.get_all()

    # ---------------------------------------------------------
    # OBTENER
    # ---------------------------------------------------------
    def obtener_mantenimiento_programado(self, **kwargs):
        """
        Obtiene un mantenimiento programado por cualquier campo.
        Ejemplos:
            obtener_mantenimiento_programado(id_programado=1)
            obtener_mantenimiento_programado(maquina_id=3)
        Retorna None si no existe.
        """
        return MantenimientoProgramadoRepository.get_by_id(**kwargs)

    # ---------------------------------------------------------
    # OBTENER POR MÁQUINA
    # ---------------------------------------------------------
    def obtener_mantenimientos_por_maquina(self, id_maquina: int):
        """
        Obtiene todos los mantenimientos programados asociados a una máquina.
        Ejemplo:
            obtener_mantenimientos_por_maquina(5)
        """
        return MantenimientoProgramadoRepository.get_by_maquina(id_maquina)

    # ---------------------------------------------------------
    # ACTUALIZAR (PUT o PATCH)
    # ---------------------------------------------------------
    def actualizar_mantenimiento_programado(self, id_programado: int, data: dict, parcial: bool = True):
        """
        Actualiza un mantenimiento programado:
        - `parcial=True` → actualización tipo PATCH
        - `parcial=False` → actualización tipo PUT
        - Valida los datos con el serializer (parcial o completo)
        - Regla de negocio: si cambia la máquina, verificar existencia
        - Guarda mediante el repository
        - Retorna datos actualizados serializados
        """
        mantenimiento = MantenimientoProgramadoRepository.get_by_id(id_programado=id_programado)

        if not mantenimiento:
            raise ValidationError({
                "id_programado": "No se encontró el mantenimiento programado a actualizar."
            })

        serializer = MantenimientoProgramadoSerializer(
            instance=mantenimiento,
            data=data,
            partial=parcial
        )
        serializer.is_valid(raise_exception=True)

        maquina = serializer.validated_data.get("maquina")

        # Regla de negocio: validar máquina si se envía
        if maquina and not MaquinariaRepository.get_by(id_maquina=maquina.id):
            raise ValidationError({
                "maquina": "La máquina asociada no existe."
            })

        mantenimiento_actualizado = MantenimientoProgramadoRepository.update(
            id_programado=id_programado,
            **serializer.validated_data
        )

        return MantenimientoProgramadoSerializer(mantenimiento_actualizado).data

    # ---------------------------------------------------------
    # ELIMINAR
    # ---------------------------------------------------------
    def eliminar_mantenimiento_programado(self, id_programado: int):
        """
        Elimina un mantenimiento programado por su ID.
        - Verifica existencia
        - Lanza error si no existe
        - Retorna True al eliminar correctamente
        """
        eliminado = MantenimientoProgramadoRepository.delete(id_programado)

        if not eliminado:
            raise ValidationError({
                "id_programado": "No se encontró el mantenimiento programado a eliminar."
            })

        return True

    # ---------------------------------------------------------
    # OBTENER POR MÁQUINA
    # ---------------------------------------------------------
    def obtener_programados_por_maquina(self, id_maquina: int):
        """
        Obtiene todos los mantenimientos programados asociados a una máquina.
        """
        return MantenimientoProgramadoRepository.get_by_maquina(id_maquina)

    # ---------------------------------------------------------
    # OBTENER POR MÁQUINA Y TIPO
    # ---------------------------------------------------------
    def obtener_mantenimiento_programado_por_maquina_y_tipo(self, id_maquina: int, tipo: str):
        """
        Obtiene un mantenimiento programado para una máquina específica y tipo.
        Ejemplo:
            obtener_mantenimiento_programado_por_maquina_y_tipo(5, 'preventivo')
        Retorna None si no existe.
        """
        return MantenimientoProgramadoRepository.get_by_maquina_y_tipo(id_maquina, tipo)