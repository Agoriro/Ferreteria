"""
Puerto (Interface) para repositorio de días de entrega por proveedor.
Principio SOLID: Dependency Inversion - Dependemos de abstracción, no implementación.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from uuid import UUID
from domain.schemas.dias_entrega_proveedor_schema import DiasEntregaProveedorCreate, DiasEntregaProveedorUpdate


class DiasEntregaProveedorRepositoryPort(ABC):
    """Interface que define el contrato para persistencia de días de entrega por proveedor."""
    
    @abstractmethod
    async def create(self, data: DiasEntregaProveedorCreate):
        """Crea un nuevo registro de días de entrega."""
        pass
    
    @abstractmethod
    async def get_by_id(self, record_id: UUID):
        """Obtiene registro por ID."""
        pass
    
    @abstractmethod
    async def get_by_empresa_nit(self, empresa: str, nit_proveedor: str):
        """Obtiene registro por empresa y NIT del proveedor."""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> Tuple[List, int]:
        """Lista todos los registros con paginación."""
        pass
    
    @abstractmethod
    async def get_by_empresa(self, empresa: str, skip: int = 0, limit: int = 100) -> Tuple[List, int]:
        """Lista registros filtrados por empresa."""
        pass
    
    @abstractmethod
    async def update(self, record_id: UUID, data: DiasEntregaProveedorUpdate):
        """Actualiza un registro."""
        pass
    
    @abstractmethod
    async def delete(self, record_id: UUID) -> bool:
        """Elimina un registro permanentemente."""
        pass


