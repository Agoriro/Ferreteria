"""
Puerto (Interface) para repositorio de roles.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.schemas.role_schema import RoleCreate, RoleUpdate


class RoleRepositoryPort(ABC):
    """Interface para persistencia de roles."""
    
    @abstractmethod
    async def create(self, role_data: RoleCreate):
        """Crea un nuevo rol."""
        pass
    
    @abstractmethod
    async def get_by_id(self, role_id: int):
        """Obtiene rol por ID."""
        pass
    
    @abstractmethod
    async def get_by_name(self, nombre_rol: str):
        """Obtiene rol por nombre."""
        pass
    
    @abstractmethod
    async def get_all(self) -> List:
        """Lista todos los roles."""
        pass
    
    @abstractmethod
    async def update(self, role_id: int, role_data: RoleUpdate):
        """Actualiza un rol."""
        pass
