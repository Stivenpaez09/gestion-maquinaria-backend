from decimal import Decimal

from rest_framework.exceptions import NotFound, ValidationError

from proyecto_maquinaria.models.proyecto_maquinaria import ProyectoMaquinaria
from proyecto_maquinaria.repositories.proyecto_maquinaria_repository import ProyectoMaquinariaRepository
from proyecto_maquinaria.serializers.proyecto_maquinaria_serializer import ProyectoMaquinariaSerializer
from proyecto_maquinaria.services.proyecto_maquinaria_service_interface import IProyectoMaquinariaService


class ProyectoMaquinariaService(IProyectoMaquinariaService):
    """
    Servicio profesional para la gestión de asignaciones de máquinas a proyectos.
    Centraliza lógica de negocio:
    - Validación con serializer
    - Reglas de negocio (máquina no asignada a proyectos activos)
    - Persistencia mediante repository
    """

    # ----------------------------------------------------------------------
    # Listar
    # ----------------------------------------------------------------------
    def listar_asignaciones(self):
        """Retorna todas las asignaciones de máquinas a proyectos."""
        return ProyectoMaquinariaRepository.get_all()

    # ----------------------------------------------------------------------
    # Obtener una asignación
    # ----------------------------------------------------------------------
    def obtener_asignacion(self, id_proyecto_maquinaria: int):
        """Obtiene una asignación por ID. Lanza NotFound si no existe."""
        asignacion = ProyectoMaquinariaRepository.get_by_id(id_proyecto_maquinaria=id_proyecto_maquinaria)
        if asignacion is None:
            raise NotFound(detail=f"La asignación con ID {id_proyecto_maquinaria} no existe.")
        return asignacion

    # ----------------------------------------------------------------------
    # Crear
    # ----------------------------------------------------------------------
    def crear_asignacion(self, data: dict):
        """
        Crea una nueva asignación de máquina a proyecto.

        Pasos:
        1. Valida datos con serializer
        2. Persiste mediante repository
        """
        serializer = ProyectoMaquinariaSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        asignacion = ProyectoMaquinariaRepository.create(**serializer.validated_data)
        return ProyectoMaquinariaSerializer(asignacion).data

    # ----------------------------------------------------------------------
    # Actualizar
    # ----------------------------------------------------------------------
    def actualizar_asignacion(self, id_proyecto_maquinaria: int, data: dict):
        """
        Actualiza una asignación existente.

        Pasos:
        1. Verifica existencia
        2. Valida datos parcialmente
        3. Actualiza vía repository
        """
        asignacion = self.obtener_asignacion(id_proyecto_maquinaria=id_proyecto_maquinaria)

        serializer = ProyectoMaquinariaSerializer(
            instance=asignacion,
            data=data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        asignacion_actualizada = ProyectoMaquinariaRepository.update(
            id_proyecto_maquinaria=id_proyecto_maquinaria,
            **serializer.validated_data
        )

        return ProyectoMaquinariaSerializer(asignacion_actualizada).data

    # ----------------------------------------------------------------------
    # Eliminar
    # ----------------------------------------------------------------------
    def eliminar_asignacion(self, id_proyecto_maquinaria: int):
        """
        Elimina una asignación por su ID.
        Lanza error si no existe.
        """
        asignacion = self.obtener_asignacion(id_proyecto_maquinaria)
        ProyectoMaquinariaRepository.delete(id_proyecto_maquinaria)
        return True

    # ----------------------------------------------------------------------
    # Actualizar horas acumuladas
    # ----------------------------------------------------------------------
    def sumar_horas_acumuladas(self, proyecto_maquinaria: ProyectoMaquinaria,
                               horas_a_sumar: Decimal) -> ProyectoMaquinaria:
        """
        Suma horas al ProyectoMaquinaria asociado.

        Reglas:
        - No permitir sumar si ya llegó al total y está finalizado.
        - Si estaba finalizado pero no ha alcanzado las horas totales, se reactiva.
        - Si llega a las horas totales, se marca finalizado automáticamente.
        - Devuelve la instancia actualizada de ProyectoMaquinaria.
        """

        # -----------------------------------------
        # Validaciones
        # -----------------------------------------
        if not proyecto_maquinaria or not isinstance(proyecto_maquinaria, ProyectoMaquinaria):
            raise NotFound(detail="La asignación de proyecto-maquinaria no existe.")

        # Asegurar Decimal
        horas_a_sumar = Decimal(horas_a_sumar)

        horas_actuales = proyecto_maquinaria.horas_acumuladas
        horas_totales = proyecto_maquinaria.horas_totales

        # -----------------------------------------
        # Reglas de negocio sobre finalizado / horas
        # -----------------------------------------

        # Si está finalizado y ya cumplió las horas → no permitir sumar más
        if proyecto_maquinaria.finalizado and horas_actuales >= horas_totales:
            raise ValidationError("La máquina ya completó las horas pactadas para este proyecto.")

        # Si está finalizado pero todavía no alcanza el total (caso muy raro)
        if proyecto_maquinaria.finalizado and horas_actuales < horas_totales:
            proyecto_maquinaria.finalizado = False

        # Sumar horas (sin exceder total)
        nuevas_horas = horas_actuales + horas_a_sumar

        if nuevas_horas >= horas_totales:
            nuevas_horas = horas_totales
            proyecto_maquinaria.finalizado = True

        # -----------------------------------------
        # Guardar cambios
        # -----------------------------------------

        asignacion_actualizada = ProyectoMaquinariaRepository.update(
            id_proyecto_maquinaria=proyecto_maquinaria.id_proyecto_maquinaria,
            horas_acumuladas=nuevas_horas,
            finalizado=proyecto_maquinaria.finalizado
        )

        return asignacion_actualizada

    def obtener_ultimo_proyecto_por_maquina(self, id_maquina: int):
      """
      Obtiene el último proyecto asociado a una máquina.
      
      Ejemplo:
          obtener_ultimo_proyecto_por_maquina(5)
      
      Retorna None si no existe.
      """
      return ProyectoMaquinariaRepository.get_last_by_maquina(id_maquina)