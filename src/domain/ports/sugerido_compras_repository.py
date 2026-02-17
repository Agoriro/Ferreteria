"""
Puerto (interfaz) para el repositorio de Sugerido de Compras.
Principio SOLID: Dependency Inversion - Define contrato abstracto.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from datetime import date

from domain.schemas.sugerido_compras_schema import (
    SugeridoComprasCreate,
    SugeridoComprasUpdate,
    SugeridoComprasResponse,
    StatusSugerido
)


class SugeridoComprasRepositoryPort(ABC):
    """Puerto abstracto para repositorio de Sugerido de Compras."""
    
    @abstractmethod
    async def create(self, data: SugeridoComprasCreate) -> SugeridoComprasResponse:
        """Crear un nuevo registro."""
        pass
    
    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[SugeridoComprasResponse]:
        """Obtener un registro por ID."""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[SugeridoComprasResponse]:
        """Obtener todos los registros con paginación."""
        pass
    
    @abstractmethod
    async def get_by_status(self, status: StatusSugerido) -> List[SugeridoComprasResponse]:
        """Obtener registros por status."""
        pass
    
    @abstractmethod
    async def update(self, id: UUID, data: SugeridoComprasUpdate) -> Optional[SugeridoComprasResponse]:
        """Actualizar un registro."""
        pass
    
    @abstractmethod
    async def update_status(self, id: UUID, status: StatusSugerido) -> Optional[SugeridoComprasResponse]:
        """Actualizar solo el status de un registro."""
        pass
    
    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """Eliminar un registro."""
        pass
    
    @abstractmethod
    async def delete_by_status(self, status: StatusSugerido) -> int:
        """Eliminar registros por status. Retorna cantidad eliminada."""
        pass
    
    @abstractmethod
    async def bulk_update_created_to_requested(self) -> int:
        """Actualizar todos los registros con status 'Created' a 'Requested'. Retorna cantidad actualizada."""
        pass
    
    @abstractmethod
    async def generar_sugerido(
        self,
        fecha_inicial: date,
        fecha_final: date,
        grupo3: Optional[str] = None,
        grupo4: Optional[str] = None,
        grupo5: Optional[str] = None
    ) -> List[SugeridoComprasResponse]:
        """
        Ejecutar el proceso de generación de sugerido de compras.
        Retorna los registros con status = 'Created'.
        """
        pass
    
    @abstractmethod
    async def bulk_create(self, items: List[SugeridoComprasCreate]) -> int:
        """Crear múltiples registros. Retorna cantidad creada."""
        pass
    
    @abstractmethod
    async def get_requested_by_tercero(self, identificacion_tercero: Optional[str] = None) -> List[SugeridoComprasResponse]:
        """
        Obtener registros con status 'Requested'.
        Si se proporciona identificacion_tercero, filtra por ese valor.
        """
        pass
    
    @abstractmethod
    async def bulk_update_proveedor(self, items: List[dict]) -> List[UUID]:
        """
        Actualizar cantidad_proveedor, valor_unitario_proveedor y cambiar status a 'Processed'.
        Retorna lista de IDs actualizados.
        """
        pass
    
    @abstractmethod
    async def get_processed(self) -> List[dict]:
        """
        Obtener registros con status 'Processed' con campos reducidos:
        empresa, proveedor, cod_prod, descripcion, unidad_medida,
        cantidad_proveedor, valor_unitario_proveedor.
        """
        pass
    
    @abstractmethod
    async def bulk_update_to_exported(self, ids: List[UUID], doc_info_map: dict = None) -> List[UUID]:
        """
        Actualizar múltiples registros a status 'Exported' y guardar datos del documento de exportación.
        Retorna lista de IDs actualizados.
        """
        pass
    
    @abstractmethod
    async def get_max_documento_oc(self) -> int:
        """
        Obtener el máximo Numero_Documento de Vista_Auxiliar_Movimientos_Inventario
        donde Tipo_Documento = 'OC' y prefijo = 'CO'.
        """
        pass
    
    @abstractmethod
    async def get_productos_iva(self, cod_prods: List[str]) -> dict:
        """
        Obtener IVA de Vista_Tabla_Inventarios por códigos de producto.
        Retorna dict {cod_prod: iva}
        """
        pass
    
    @abstractmethod
    async def get_sugeridos_for_export(self, ids: List[UUID]) -> List[dict]:
        """
        Obtener registros completos de sugerido_compras por IDs.
        Retorna lista de dicts con campos necesarios para generar órdenes de compra.
        """
        pass
    
    @abstractmethod
    async def get_reporte(
        self,
        fecha_inicial: date,
        fecha_final: date,
        identificacion_tercero: Optional[str] = None,
        status_filter: Optional[str] = None
    ) -> List[dict]:
        """
        Obtener reporte de sugerido de compras filtrado por rango de fechas en updated_at.
        Opcionalmente filtra por identificacion_tercero y status.
        """
        pass


