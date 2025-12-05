from decimal import Decimal

from rest_framework.exceptions import NotFound

from alarmas.repositories.alarma_repository import AlarmaRepository
from alarmas.serializers.alarma_serializer import AlarmaSerializer
from alarmas.services.alarma_service_interface import IAlarmaService
from mantenimientos.services.mantenimiento_service import MantenimientoService
from mantenimientos_programados.services.mantenimiento_programado_service import MantenimientoProgramadoService
from maquinarias.services.maquinaria_service import MaquinariaService


class AlarmaService(IAlarmaService):
    """
    Servicio de lógica de negocio para la gestión de Alarmas.
    
    Responsabilidades:
    - Validar horas de mantenimiento programado vs. horas totales
    - Generar alarmas automáticas (crítica, media)
    - Gestionar el ciclo de vida de las alarmas (CRUD)
    - Consultas y estadísticas para dashboard
    """

    def __init__(self):
        """Inyección de dependencias de otros servicios."""
        self.mantenimiento_service = MantenimientoService()
        self.mantenimiento_programado_service = MantenimientoProgramadoService()
        self.maquinaria_service = MaquinariaService()

    # =========================================================================
    # MÉTODO PRINCIPAL: VALIDAR Y GENERAR ALARMAS
    # =========================================================================

    def validar_y_generar_alarmas(self, id_maquina: int):
        """
        Nueva lógica para generar alarmas:

        - Una máquina puede tener múltiples mantenimientos programados del mismo tipo.
        - Para cada mantenimiento programado:
            * Se obtiene el último mantenimiento real vinculado (maquina + programado)
            * Se calcula horas_proximas = horas_realizadas + intervalo_horas
            * Se compara contra horas_totales de la máquina
            * Se genera alarma CRÍTICA o MEDIA
        """

        # 1. Obtener la máquina
        maquina = self.maquinaria_service.obtener_maquinaria(id_maquina=id_maquina)
        if not maquina:
            raise NotFound(f"Máquina con ID {id_maquina} no existe.")

        horas_totales = Decimal(str(maquina.horas_totales))
        alarmas_creadas = []

        # 2. Obtener todos los mantenimientos programados de la máquina
        programados = (
            self.mantenimiento_programado_service
            .obtener_programados_por_maquina(id_maquina=id_maquina)
        )

        if not programados:
            return {
                "id_maquina": id_maquina,
                "alarmas_creadas": [],
                "cantidad": 0,
                "mensaje": "La máquina no tiene mantenimientos programados"
            }

        # 3. Procesar cada mantenimiento programado
        for programado in programados:

            # Obtener el último mantenimiento real de esta máquina asociado a este programado
            ultimo_mantenimiento = (
                self.mantenimiento_service
                .obtener_ultimo_mantenimiento_por_maquina_y_programado(
                    id_maquina=id_maquina,
                    id_programado=programado.id_programado
                )
            )

            # Si nunca se ha hecho un mantenimiento para este programado → saltar
            if not ultimo_mantenimiento:
                continue

            # 4. Cálculo de horas
            horas_realizadas = Decimal(str(ultimo_mantenimiento.horas_realizadas))
            intervalo_horas = Decimal(str(programado.intervalo_horas))

            horas_proximas = horas_realizadas + intervalo_horas
            diferencia = horas_proximas - horas_totales

            # 5. Crear alarmas
            tipo = programado.tipo  # preventivo / predictivo / correctivo, etc.

            # CRÍTICA
            if diferencia <= 0:
                self.maquinaria_service.actualizar_estado_maquinaria(
                    id_maquina=id_maquina,
                    estado="fuera de servicio"
                )
                alarma = self._crear_alarma(
                    id_maquina=id_maquina,
                    tipo="mantenimiento",
                    nivel="crítica",
                    descripcion=(
                        f"Es hora de realizar el mantenimiento {tipo} "
                        f"(programado #{programado.id_programado}). "
                        f"Horas alcanzadas: {horas_totales}"
                    )
                )
                alarmas_creadas.append(alarma)

            # MEDIA (faltan 20 horas o menos)
            elif 0 < diferencia <= 20:
                alarma = self._crear_alarma(
                    id_maquina=id_maquina,
                    tipo="mantenimiento",
                    nivel="media",
                    descripcion=(
                        f"En {diferencia:.2f} horas se debe realizar el mantenimiento {tipo} "
                        f"(programado #{programado.id_programado}) "
                        f"de la máquina {id_maquina}."
                    )
                )
                alarmas_creadas.append(alarma)

        # 6. Respuesta
        return {
            "id_maquina": id_maquina,
            "alarmas_creadas": alarmas_creadas,
            "cantidad": len(alarmas_creadas),
            "mensaje": (
                f"Se crearon {len(alarmas_creadas)} alarma(s)"
                if alarmas_creadas else
                "No se generaron alarmas"
            )
        }

    # =========================================================================
    # UTILIDAD INTERNA: CREAR ALARMA (PERSISTE EN BD)
    # =========================================================================

    def _crear_alarma(self, id_maquina: int, tipo: str, nivel: str, descripcion: str):
        """
        Crea y PERSISTE una alarma en la base de datos.
        
        Args:
            id_maquina: ID de la máquina
            tipo: tipo de alarma ('mantenimiento')
            nivel: nivel de severidad ('crítica', 'media')
            descripcion: descripción de la alarma
            
        Returns:
            dict: datos serializados de la alarma creada (incluyendo id_alarma)
        """
        alarma = AlarmaRepository.create(
            maquina_id=id_maquina,
            tipo=tipo,
            nivel=nivel,
            descripcion=descripcion,
            vista=False
        )
        return AlarmaSerializer(alarma).data

    # =========================================================================
    # CRUD: LISTAR
    # =========================================================================

    def listar_alarmas(self):
        """Retorna todas las alarmas registradas."""
        return AlarmaRepository.get_all()

    # =========================================================================
    # CRUD: OBTENER UNA
    # =========================================================================

    def obtener_alarma(self, id_alarma: int):
        """
        Obtiene una alarma por ID.
        Lanza NotFound si no existe.
        """
        alarma = AlarmaRepository.get_by_id(id_alarma=id_alarma)
        
        if not alarma:
            raise NotFound(f"Alarma con ID {id_alarma} no existe.")
        
        return alarma

    # =========================================================================
    # MARCAR COMO VISTA
    # =========================================================================

    def marcar_como_vista(self, id_alarma: int):
        """
        Marca una alarma como vista.
        Lanza NotFound si no existe.
        """
        alarma = AlarmaRepository.update(id_alarma, vista=True)
        
        if not alarma:
            raise NotFound(f"Alarma con ID {id_alarma} no existe.")
        
        return AlarmaSerializer(alarma).data

    # =========================================================================
    # ELIMINAR
    # =========================================================================

    def eliminar_alarma(self, id_alarma: int):
        """
        Elimina una alarma.
        Lanza NotFound si no existe.
        """
        existe = AlarmaRepository.delete(id_alarma)
        
        if not existe:
            raise NotFound(f"Alarma con ID {id_alarma} no existe.")
        
        return {"mensaje": f"Alarma {id_alarma} eliminada correctamente"}

    # =========================================================================
    # CONSULTAS ESPECÍFICAS
    # =========================================================================

    def obtener_alarmas_por_maquina(self, id_maquina: int):
        """Obtiene todas las alarmas de una máquina."""
        return AlarmaRepository.get_by_maquina(id_maquina)

    def obtener_alarmas_no_vistas(self):
        """Obtiene todas las alarmas sin ver."""
        return AlarmaRepository.get_no_vistas()

    def obtener_cantidad_alarmas_no_vistas(self):
        """Obtiene la cantidad de alarmas sin ver."""
        return AlarmaRepository.contar_no_vistas()

    def obtener_alarmas_criticas(self):
        """Obtiene todas las alarmas de nivel crítico."""
        return AlarmaRepository.get_criticas()

    def obtener_alarmas_por_tipo(self, tipo: str):
        """Obtiene alarmas filtradas por tipo."""
        return AlarmaRepository.get_by_tipo(tipo)

    # =========================================================================
    # ESTADÍSTICAS PARA DASHBOARD
    # =========================================================================

    def obtener_estadisticas(self):
        """
        Retorna estadísticas de alarmas para el dashboard.
        """
        return {
            "total_no_vistas": AlarmaRepository.contar_no_vistas(),
            "total_criticas": len(AlarmaRepository.get_criticas()),
            "conteo_por_nivel": list(AlarmaRepository.contar_por_nivel()),
            "conteo_por_tipo": list(AlarmaRepository.contar_por_tipo()),
            "ultimas_10": AlarmaSerializer(
                AlarmaRepository.get_ultimas(limit=10),
                many=True
            ).data
        }