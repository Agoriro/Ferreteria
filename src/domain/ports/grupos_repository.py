"""
Puertos (interfaces) para los repositorios de Grupos.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from domain.schemas.grupos_schema import (
    GruposTresCreate, GruposTresUpdate, GruposTresResponse,
    GruposCuatroCreate, GruposCuatroUpdate, GruposCuatroResponse,
    GruposCincoCreate, GruposCincoUpdate, GruposCincoResponse
)


class GruposTresRepositoryPort(ABC):
    """Puerto para el repositorio de Grupos Tres."""
    
    @abstractmethod
    async def create(self, data: GruposTresCreate) -> GruposTresResponse:
        """Crear un nuevo grupo."""
        pass
    
    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[GruposTresResponse]:
        """Obtener grupo por ID."""
        pass
    
    @abstractmethod
    async def get_by_nombre(self, nombre: str) -> Optional[GruposTresResponse]:
        """Obtener grupo por nombre."""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[GruposTresResponse]:
        """Obtener todos los grupos."""
        pass
    
    @abstractmethod
    async def count(self) -> int:
        """Contar total de grupos."""
        pass
    
    @abstractmethod
    async def update(self, id: UUID, data: GruposTresUpdate) -> Optional[GruposTresResponse]:
        """Actualizar un grupo."""
        pass
    
    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """Eliminar un grupo."""
        pass


class GruposCuatroRepositoryPort(ABC):
    """Puerto para el repositorio de Grupos Cuatro."""
    
    @abstractmethod
    async def create(self, data: GruposCuatroCreate) -> GruposCuatroResponse:
        """Crear un nuevo grupo."""
        pass
    
    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[GruposCuatroResponse]:
        """Obtener grupo por ID."""
        pass
    
    @abstractmethod
    async def get_by_nombre(self, nombre: str) -> Optional[GruposCuatroResponse]:
        """Obtener grupo por nombre."""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[GruposCuatroResponse]:
        """Obtener todos los grupos."""
        pass
    
    @abstractmethod
    async def count(self) -> int:
        """Contar total de grupos."""
        pass
    
    @abstractmethod
    async def update(self, id: UUID, data: GruposCuatroUpdate) -> Optional[GruposCuatroResponse]:
        """Actualizar un grupo."""
        pass
    
    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """Eliminar un grupo."""
        pass


class GruposCincoRepositoryPort(ABC):
    """Puerto para el repositorio de Grupos Cinco."""
    
    @abstractmethod
    async def create(self, data: GruposCincoCreate) -> GruposCincoResponse:
        """Crear un nuevo grupo."""
        pass
    
    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[GruposCincoResponse]:
        """Obtener grupo por ID."""
        pass
    
    @abstractmethod
    async def get_by_nombre(self, nombre: str) -> Optional[GruposCincoResponse]:
        """Obtener grupo por nombre."""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[GruposCincoResponse]:
        """Obtener todos los grupos."""
        pass
    
    @abstractmethod
    async def count(self) -> int:
        """Contar total de grupos."""
        pass
    
    @abstractmethod
    async def update(self, id: UUID, data: GruposCincoUpdate) -> Optional[GruposCincoResponse]:
        """Actualizar un grupo."""
        pass
    
    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """Eliminar un grupo."""
        pass
