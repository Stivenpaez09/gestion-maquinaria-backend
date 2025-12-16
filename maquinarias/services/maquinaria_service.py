import os
import uuid
from decimal import Decimal
from typing import Optional

from django.core.files.uploadedfile import UploadedFile
from rest_framework.exceptions import ValidationError, NotFound

from mantenimientos.services.mantenimiento_service import MantenimientoService
from mantenimientos_programados.services.mantenimiento_programado_service import MantenimientoProgramadoService
from maquinarias.models.maquinaria import Maquinaria
from maquinarias.serializers.maquinaria_serializer import MaquinariaSerializer
from maquinarias.repositories.maquinaria_repository import MaquinariaRepository
from maquinarias.services.maquinaria_service_interface import IMaquinariaService
from proyecto_maquinaria.services.proyecto_maquinaria_service import ProyectoMaquinariaService
from servimacons import settings


class MaquinariaService(IMaquinariaService):
    """
    Servicio de lógica de negocio para la gestión de Maquinarias.
    Coordina validación (serializer) y persistencia (repository),
    aplicando reglas de negocio como la unicidad de la serie.
    """

    def __init__(self):
        self.mantenimiento_service = MantenimientoService()
        self.mantenimiento_programado_service = MantenimientoProgramadoService()
        self.proyecto_maquinaria_service = ProyectoMaquinariaService()

    # ----------------------------------------------------------------------
    # UTILIDAD: Guardar foto físicamente
    # ----------------------------------------------------------------------
    def _guardar_foto(self, foto_file: Optional[UploadedFile]) -> Optional[str]:
        """
        Guarda la foto en maquinarias/photos/
        Retorna la URL absoluta final que se almacenará en BD.
        """
        if not foto_file:
            return None

        # Carpeta dentro de media/
        carpeta_relativa = "maquinarias/photos"
        carpeta_absoluta = os.path.join(settings.MEDIA_ROOT, carpeta_relativa)

        # Crear carpeta si no existe
        os.makedirs(carpeta_absoluta, exist_ok=True)

        # Nombre único
        extension = foto_file.name.split('.')[-1]
        filename = f"{uuid.uuid4()}.{extension}"

        # Ruta física en disco
        ruta_fisica = os.path.join(carpeta_absoluta, filename)

        # Guardar archivo físicamente
        with open(ruta_fisica, "wb+") as destino:
            for chunk in foto_file.chunks():
                destino.write(chunk)

        # URL interna MEDIA_URL
        url_final = f"{settings.MEDIA_URL}{carpeta_relativa}/{filename}"

        return url_final

    # ---------------------------------------------------------
    # CREAR
    # ---------------------------------------------------------
    def crear_maquinaria(self, data: dict):
        """
        Crea una maquinaria:
        - Valida los datos con el serializer
        - Regla de negocio: evitar duplicado por 'serie'
        - Guarda mediante el repository
        - Retorna datos serializados
        """
        data = data.copy()
        foto_file = data.pop("foto", None)
        # ----- Normalización universal (soporta archivo único o array) -----
        if isinstance(foto_file, list):
            foto_file = foto_file[0] if foto_file else None

        serializer = MaquinariaSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        serie = serializer.validated_data.get("serie")

        # Regla: evitar duplicado de serie
        if serie and MaquinariaRepository.get_by(serie = serie):
            raise ValidationError({
                "serie": "Esta serie ya está registrada."
            })

        # Si viene una foto → guardarla en disco
        if foto_file:
            ruta_foto = self._guardar_foto(foto_file)
            serializer.validated_data["foto"] = ruta_foto

        maquinaria = MaquinariaRepository.create(
            **serializer.validated_data
        )

        return MaquinariaSerializer(maquinaria).data

    # ---------------------------------------------------------
    # LISTAR
    # ---------------------------------------------------------
    def listar_maquinarias(self):
        """Retorna todas las maquinarias registradas."""
        return MaquinariaRepository.get_all()

    # ---------------------------------------------------------
    # OBTENER
    # ---------------------------------------------------------
    def obtener_maquinaria(self, **kwargs):
        """
        Obtiene una maquinaria por cualquier campo.
        Ejemplos:
            obtener_maquinaria(id_maquina=1)
            obtener_maquinaria(serie="ABC123")
        Lanza error si no existe.
        """
        maquinaria = MaquinariaRepository.get_by(**kwargs)

        if maquinaria is None:
            raise NotFound("La maquinaria solicitada no existe.")

        return maquinaria

    # ---------------------------------------------------------
    # ACTUALIZAR (PUT o PATCH)
    # ---------------------------------------------------------
    def actualizar_maquinaria(self, id_maquina: int, data: dict):
        """
        Actualiza una maquinaria:
        - `parcial=True` → actualización tipo PATCH
        - `parcial=False` → actualización tipo PUT
        - Valida datos con el serializer (parcial o completo)
        - Regla de negocio: si cambia la serie, verificar duplicado
        - Realiza la actualización mediante el repository
        - Retorna datos actualizados serializados
        """
        maquinaria = self.obtener_maquinaria(id_maquina=id_maquina)
        data = data.copy()
        foto_file = data.pop("foto", None)
        # ----- Normalización universal (soporta archivo único o array) -----
        if isinstance(foto_file, list):
            foto_file = foto_file[0] if foto_file else None

        if not maquinaria:
            raise NotFound("No se encontró la maquinaria a actualizar.")

        serializer = MaquinariaSerializer(
            maquinaria,
            data=data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        nueva_serie = serializer.validated_data.get("serie")

        # Regla: si cambia la serie, validar duplicado
        if nueva_serie:
            existente = MaquinariaRepository.get_by(serie=nueva_serie)
            if existente and existente.id_maquina != id_maquina:
                raise ValidationError({
                    "serie": "Otra maquinaria ya está registrada con esta serie."
                })

        # Manejo opcional de foto
        if foto_file:
            nueva_ruta = self._guardar_foto(foto_file)
            serializer.validated_data["foto"] = nueva_ruta

        maquinaria_actualizada = MaquinariaRepository.update(
            maquinaria,
            **serializer.validated_data
        )

        return maquinaria_actualizada


    # ---------------------------------------------------------
    # ACTUALIZAR HORAS TOTALES
    # ---------------------------------------------------------
    def sumar_horas_maquinaria(self, maquina: Maquinaria, horas_a_sumar: Decimal):
        """
        Suma horas al campo horas_totales de una maquinaria.

        Reglas de negocio:
        - La maquinaria debe existir
        - No se pueden sumar horas negativas
        - No se pueden sumar horas si la maquinaria está 'fuera de servicio'
        - Si queda en 0 → inconsistente para máquina operativa (evitar)

        Retorna: maquinaria actualizada serializada.
        """

        # Validar instancia
        if not maquina or not isinstance(maquina, Maquinaria):
            raise ValidationError({"maquina": "Debe proporcionar una maquinaria válida."})

        # Convertir a Decimal
        try:
            horas_a_sumar = Decimal(str(horas_a_sumar))
        except Exception:
            raise ValidationError({"horas": "Las horas deben ser un número decimal válido."})

        if horas_a_sumar <= 0:
            raise ValidationError({"horas": "Las horas a sumar deben ser mayores a 0."})

        # Regla de negocio: no sumar horas si está fuera de servicio
        if maquina.estado == "fuera de servicio":
            raise ValidationError({
                "estado": "No se pueden registrar horas en una máquina fuera de servicio."
            })

        # Llamar al repository
        maquinaria_actualizada = MaquinariaRepository.update_horas_totales(
            maquina=maquina,
            horas_a_sumar=horas_a_sumar
        )

        return maquinaria_actualizada

    # ---------------------------------------------------------
    # ACTUALIZAR HORAS TOTALES
    # ---------------------------------------------------------
    def actualizar_estado_maquinaria(self, id_maquina: int, estado: str):
        """
            Actualiza el estado de una maquinaria específica.

            Reglas de negocio:
            - La maquinaria debe existir.
            - El estado debe ser uno de los permitidos:
                ["operativa", "fuera de servicio", "en mantenimiento"]
            - No se permite actualizar con un estado vacío o nulo.
            - Si el estado no cambia, no realiza operaciones innecesarias.

            Retorna:
            - La maquinaria actualizada (instancia del modelo).
            """
        maquinaria = self.obtener_maquinaria(id_maquina=id_maquina)

        if maquinaria.estado == estado:
            return maquinaria

        if estado and estado == "fuera de servicio":
            maquinaria.estado = "fuera de servicio"

        if estado and estado == "operativa":
            maquinaria.estado = "operativa"

        if estado and estado == "en mantenimiento":
            maquinaria.estado = "en mantenimiento"

        maquinarias_actualizada = MaquinariaRepository.update_estado(maquinaria=maquinaria)
        return maquinarias_actualizada
    # ---------------------------------------------------------
    # ELIMINAR
    # ---------------------------------------------------------
    def eliminar_maquinaria(self, id_maquina: int):
        """
        Elimina una maquinaria por ID.
        Lanza error si no existe.
        Retorna True ante eliminación exitosa.
        """
        maquinaria = self.obtener_maquinaria(id_maquina=id_maquina)
        eliminado = MaquinariaRepository.delete(id_maquina)

        if not eliminado:
            raise NotFound("No se encontró la maquinaria a eliminar.")

        return True

    # =========================================================================
    # RESUMEN GENERAL DE MAQUINARIAS
    # =========================================================================

    def obtener_resumen_maquinarias(self):
        """
        Genera un resumen consolidado del estado de todas las máquinas.
        
        Métricas:
        - en_operacion: máquinas con proyecto activo (finalizado=False)
        - al_dia: máquinas con mantenimiento programado en > 48 horas
        - pendientes: máquinas con mantenimiento programado en <= 48 horas
        - vencidos: máquinas que ya alcanzaron/superaron el límite de horas
        
        Reglas:
        1. Para cada máquina, evalúa PREVENTIVO y PREDICTIVO por separado
        2. Cada tipo de mantenimiento suma 1 punto a UNA SOLA categoría
           (vencido > pendiente > al_día, en ese orden)
        3. El estado en_operacion es independiente
           (una máquina puede estar vencida Y en operación)
        
        Returns:
            {
                "en_operacion": int,
                "al_dia": int,
                "pendientes": int,
                "vencidos": int
            }
        """
        
        # Contadores
        resumen = {
            "en_operacion": 0,
            "al_dia": 0,
            "pendientes": 0,
            "vencidos": 0
        }

        # Obtener todas las máquinas
        maquinas = self.listar_maquinarias()

        # Iterar sobre cada máquina
        for maquina in maquinas:
            id_maquina = maquina.id_maquina
            horas_totales = Decimal(str(maquina.horas_totales))

            # ======================================================
            # 1. EVALUAR ESTADO DE OPERACIÓN (INDEPENDIENTE)
            # ======================================================
            ultimo_proyecto = self.proyecto_maquinaria_service.obtener_ultimo_proyecto_por_maquina(
                id_maquina=id_maquina
            )

            # Si existe proyecto activo → suma a en_operacion
            if ultimo_proyecto and not ultimo_proyecto.finalizado:
                resumen["en_operacion"] += 1

            programados = self.mantenimiento_programado_service.obtener_programados_por_maquina(id_maquina)

            if not programados:
                resumen["al_dia"] += 1
                continue

            estado_maquina = "al_dia"

            for programado in programados:

                ultimo_mantenimiento = self.mantenimiento_service.obtener_ultimo_mantenimiento_por_maquina_y_programado(
                    id_maquina=id_maquina,
                    id_programado=programado.id_programado
                )

                # Si no existe mantenimiento del tipo → ignorar
                if not ultimo_mantenimiento:
                    continue


                # ======================================================
                # CALCULAR HORAS
                # ======================================================
                horas_realizadas = Decimal(str(ultimo_mantenimiento.horas_realizadas))
                intervalo_horas = Decimal(str(programado.intervalo_horas))
                
                horas_proximas = horas_realizadas + intervalo_horas
                diferencia = horas_proximas - horas_totales

                # ======================================================
                # CLASIFICAR: VENCIDO → PENDIENTE → AL DÍA
                # (Orden obligatorio para exclusividad)
                # ======================================================
                if diferencia <= 0:
                    estado_maquina = "vencidos"
                    break  # ya es el peor estado posible

                elif 0 < diferencia <= 20:
                    if estado_maquina != "pendientes":  # no sobrescribir si ya estaba en "vencidos"
                        estado_maquina = "pendientes"
                    # NO hacemos break porque podría haber un vencido en los que faltan

                    # ---------------------------------------
                    # 4. Incrementar UNA SOLA categoría por máquina
                    # ---------------------------------------
            resumen[estado_maquina] += 1

        return resumen

    # =========================================================================
    # LISTA DE MAQUINARIAS EN OPERACION
    # =========================================================================
    def obtener_maquinarias_operacion(self):
        """
        Retorna las maquinarias actualmente en operación.
        Una maquinaria está en operación si su último proyecto no está finalizado.
        """
        maquinarias_operacion = []
        maquinas = self.listar_maquinarias()

        for maquina in maquinas:
            id_maquina = maquina.id_maquina

            ultimo_proyecto = self.proyecto_maquinaria_service.obtener_ultimo_proyecto_por_maquina(
                id_maquina=id_maquina
            )

            if ultimo_proyecto and not ultimo_proyecto.finalizado:
                maquinarias_operacion.append(maquina)

        return maquinarias_operacion

    # =========================================================================
    # LISTA DE MAQUINARIAS VENCIDAS
    # =========================================================================
    def obtener_maquinarias_vencidas(self):
        """
        Retorna maquinarias con al menos un mantenimiento programado vencido.
        VENCIDO = horas_proximas <= horas_totales
        """
        maquinarias_vencidas = []
        maquinas = self.listar_maquinarias()

        for maquina in maquinas:
            id_maquina = maquina.id_maquina
            horas_totales = Decimal(str(maquina.horas_totales))

            programados = self.mantenimiento_programado_service.obtener_programados_por_maquina(id_maquina)

            for programado in programados:

                # Obtener último mantenimiento real asociado a este programado
                ultimo = self.mantenimiento_service.obtener_ultimo_mantenimiento_por_maquina_y_programado(
                    id_maquina=id_maquina,
                    id_programado=programado.id_programado
                )

                if not ultimo:
                    continue  # Nunca se ha realizado → ignorar

                horas_realizadas = Decimal(str(ultimo.horas_realizadas))
                intervalo = Decimal(str(programado.intervalo_horas))
                horas_proximas = horas_realizadas + intervalo

                if horas_proximas <= horas_totales:
                    maquinarias_vencidas.append(maquina)
                    break

        return maquinarias_vencidas

    # =========================================================================
    # LISTA DE MAQUINARIAS PENDIENTES
    # =========================================================================
    def obtener_maquinarias_pendientes(self):
        """
        Retorna maquinarias con al menos un mantenimiento programado próximo.
        PENDIENTE = 0 < (horas_proximas - horas_totales) <= 20
        """
        maquinarias_pendientes = []
        maquinas = self.listar_maquinarias()

        for maquina in maquinas:
            id_maquina = maquina.id_maquina
            horas_totales = Decimal(str(maquina.horas_totales))

            programados = self.mantenimiento_programado_service.obtener_programados_por_maquina(id_maquina)

            for programado in programados:

                ultimo = self.mantenimiento_service.obtener_ultimo_mantenimiento_por_maquina_y_programado(
                    id_maquina=id_maquina,
                    id_programado=programado.id_programado
                )

                if not ultimo:
                    continue

                horas_realizadas = Decimal(str(ultimo.horas_realizadas))
                intervalo = Decimal(str(programado.intervalo_horas))
                horas_proximas = horas_realizadas + intervalo

                diferencia = horas_proximas - horas_totales

                # pendiente: faltan entre 1 y 20 horas
                if 0 < diferencia <= 20:
                    maquinarias_pendientes.append(maquina)
                    break

        return maquinarias_pendientes


    # =========================================================================
    # LISTA DE MAQUINARIAS AL DIA
    # =========================================================================
    def obtener_maquinarias_al_dia(self):
        """
        Retorna maquinarias que están totalmente al día.
        AL DÍA = ninguna vencida y ninguna pendiente.
        """
        maquinarias_al_dia = []
        maquinas = self.listar_maquinarias()

        for maquina in maquinas:
            id_maquina = maquina.id_maquina
            horas_totales = Decimal(str(maquina.horas_totales))

            programados = self.mantenimiento_programado_service.obtener_programados_por_maquina(id_maquina)

            estado = "al_dia"

            for programado in programados:

                ultimo = self.mantenimiento_service.obtener_ultimo_mantenimiento_por_maquina_y_programado(
                    id_maquina=id_maquina,
                    id_programado=programado.id_programado
                )

                if not ultimo:
                    continue

                horas_realizadas = Decimal(str(ultimo.horas_realizadas))
                intervalo = Decimal(str(programado.intervalo_horas))
                horas_proximas = horas_realizadas + intervalo

                diferencia = horas_proximas - horas_totales

                if horas_proximas <= horas_totales:
                    estado = "vencida"
                    break

                if 0 < diferencia <= 20:
                    estado = "pendiente"
                    break

            if estado == "al_dia":
                maquinarias_al_dia.append(maquina)

        return maquinarias_al_dia

    def listar_ultimas_maquinarias(self):
        """Retorna las ultimas maquinarias creadas o actualizadas"""
        return MaquinariaRepository.get_last_updated(limit=10)