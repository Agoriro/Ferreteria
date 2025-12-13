"""
Puerto (Interface) para repositorio de inventario excluido.
Principio SOLID: Dependency Inversion - Dependemos de abstracción, no implementación.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from uuid import UUID
from domain.schemas.inventario_excluido_schema import InventarioExcluidoCreate, InventarioExcluidoUpdate


class InventarioExcluidoRepositoryPort(ABC):
    """Interface que define el contrato para persistencia de inventario excluido."""
    
    @abstractmethod
    async def create(self, data: InventarioExcluidoCreate):
        """Crea un nuevo registro de inventario excluido."""
        pass
    
    @abstractmethod
    async def get_by_id(self, record_id: UUID):
        """Obtiene registro por ID."""
        pass
    
    @abstractmethod
    async def get_by_codigo_producto(self, codigo_producto: str):
        """Obtiene registro por código de producto."""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100, include_inactive: bool = False) -> Tuple[List, int]:
        """Lista todos los registros con paginación."""
        pass
    
    @abstractmethod
    async def update(self, record_id: UUID, data: InventarioExcluidoUpdate):
        """Actualiza un registro."""
        pass
    
    @abstractmethod
    async def toggle_status(self, record_id: UUID, new_status: bool) -> bool:
        """Cambia el estado de un registro."""
        pass
    
    @abstractmethod
    async def delete(self, record_id: UUID) -> bool:
        """Elimina un registro permanentemente."""
        pass

