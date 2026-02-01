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

