"""
Puerto (Interface) para repositorio de usuarios.
Principio SOLID: Dependency Inversion - Dependemos de abstracción, no implementación.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from domain.schemas.user_schema import UserCreate, UserUpdate


class UserRepositoryPort(ABC):
    """Interface que define el contrato para persistencia de usuarios."""
    
    @abstractmethod
    async def create(self, user_data: UserCreate, hashed_password: str):
        """Crea un nuevo usuario."""
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: int):
        """Obtiene usuario por ID."""
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str):
        """Obtiene usuario por username."""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100, include_inactive: bool = False) -> List:
        """Lista todos los usuarios."""
        pass
    
    @abstractmethod
    async def update(self, user_id: int, user_data: UserUpdate):
        """Actualiza un usuario."""
        pass
    
    @abstractmethod
    async def soft_delete(self, user_id: int) -> bool:
        """Soft delete (cambiar estado a False)."""
        pass
    
    @abstractmethod
    async def update_password(self, user_id: int, hashed_password: str) -> bool:
        """Actualiza la contraseña."""
        pass
