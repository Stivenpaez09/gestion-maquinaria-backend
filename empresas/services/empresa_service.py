from rest_framework.exceptions import ValidationError

from empresas.repositories.empresa_repository import EmpresaRepository
from empresas.serializers.empresa_serializer import EmpresaSerializer
from empresas.services.empresa_service_interface import IEmpresaService


class EmpresaService(IEmpresaService):
    """
    Servicio de lógica de negocio para la gestión de Empresas.
    Coordina validaciones (serializer) y persistencia (repository),
    aplicando reglas de negocio y retornando instancias del modelo
    sin serializar (la serialización se hace en el ViewSet).
    """

    # ---------------------------------------------------------
    # CREAR
    # ---------------------------------------------------------
    def crear_empresa(self, data: dict):
        """
        Crea una empresa:
        - Valida datos con el serializer
        - Aplica reglas de negocio (si las hubiera)
        - Guarda la empresa mediante el repository
        - Retorna la instancia creada (NO serializada)
        """
        serializer = EmpresaSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        empresa = EmpresaRepository.create(**serializer.validated_data)
        return empresa

    # ---------------------------------------------------------
    # LISTAR
    # ---------------------------------------------------------
    def listar_empresas(self):
        """Retorna todas las empresas registradas."""
        return EmpresaRepository.get_all()

    # ---------------------------------------------------------
    # OBTENER
    # ---------------------------------------------------------
    def obtener_empresa(self, **kwargs):
        """
        Obtiene una empresa por cualquier campo.
        Ejemplos:
            obtener_empresa(id_empresa=1)
            obtener_empresa(nit="900123123")
        Retorna None si no existe.
        """
        return EmpresaRepository.get_by_id(**kwargs)

    # ---------------------------------------------------------
    # ACTUALIZAR (PUT o PATCH)
    # ---------------------------------------------------------
    def actualizar_empresa(self, id_empresa: int, data: dict, parcial: bool = True):
        """
        Actualiza una empresa:
        - `parcial=True` → PATCH
        - `parcial=False` → PUT
        - Valida los datos con el serializer (parcial o completo)
        - Aplica reglas de negocio si corresponde
        - Retorna la instancia actualizada (NO serializada)
        """
        empresa = EmpresaRepository.get_by_id(id_empresa=id_empresa)

        if not empresa:
            raise ValidationError({
                "id_empresa": "No se encontró la empresa a actualizar."
            })

        serializer = EmpresaSerializer(
            instance=empresa,
            data=data,
            partial=parcial
        )
        serializer.is_valid(raise_exception=True)

        empresa_actualizada = EmpresaRepository.update(
            id_empresa=id_empresa,
            **serializer.validated_data
        )

        return empresa_actualizada

    # ---------------------------------------------------------
    # ELIMINAR
    # ---------------------------------------------------------
    def eliminar_empresa(self, id_empresa: int):
        """
        Elimina una empresa por su ID.
        - Verifica existencia
        - Lanza error si no existe
        - Retorna True al eliminar correctamente
        """
        eliminado = EmpresaRepository.delete(id_empresa)

        if not eliminado:
            raise ValidationError({
                "id_empresa": "No se encontró la empresa a eliminar."
            })

        return True
