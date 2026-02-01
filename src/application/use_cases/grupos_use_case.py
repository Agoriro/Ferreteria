"""
Casos de uso para Grupos (Tres, Cuatro, Cinco).
"""
from typing import Optional, List
from uuid import UUID

from domain.ports.grupos_repository import (
    GruposTresRepositoryPort,
    GruposCuatroRepositoryPort,
    GruposCincoRepositoryPort
)
from domain.schemas.grupos_schema import (
    GruposTresCreate, GruposTresUpdate, GruposTresResponse, GruposTresListResponse,
    GruposCuatroCreate, GruposCuatroUpdate, GruposCuatroResponse, GruposCuatroListResponse,
    GruposCincoCreate, GruposCincoUpdate, GruposCincoResponse, GruposCincoListResponse
)


class GruposTresUseCase:
    """Casos de uso para Grupos Tres."""
    
    def __init__(self, repository: GruposTresRepositoryPort):
        self.repository = repository
    
    async def create(self, data: GruposTresCreate) -> GruposTresResponse:
        """Crear un nuevo grupo."""
        existing = await self.repository.get_by_nombre(data.grupo_tres)
        if existing:
            raise ValueError(f"Ya existe un grupo con el nombre '{data.grupo_tres}'")
        return await self.repository.create(data)
    
    async def get_by_id(self, id: UUID) -> Optional[GruposTresResponse]:
        """Obtener grupo por ID."""
        return await self.repository.get_by_id(id)
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> GruposTresListResponse:
        """Obtener todos los grupos."""
        items = await self.repository.get_all(skip, limit)
        total = await self.repository.count()
        return GruposTresListResponse(items=items, total=total)
    
    async def update(self, id: UUID, data: GruposTresUpdate) -> Optional[GruposTresResponse]:
        """Actualizar un grupo."""
        if data.grupo_tres:
            existing = await self.repository.get_by_nombre(data.grupo_tres)
            if existing and existing.id != id:
                raise ValueError(f"Ya existe otro grupo con el nombre '{data.grupo_tres}'")
        return await self.repository.update(id, data)
    
    async def delete(self, id: UUID) -> bool:
        """Eliminar un grupo."""
        return await self.repository.delete(id)


class GruposCuatroUseCase:
    """Casos de uso para Grupos Cuatro."""
    
    def __init__(self, repository: GruposCuatroRepositoryPort):
        self.repository = repository
    
    async def create(self, data: GruposCuatroCreate) -> GruposCuatroResponse:
        """Crear un nuevo grupo."""
        existing = await self.repository.get_by_nombre(data.grupo_cuatro)
        if existing:
            raise ValueError(f"Ya existe un grupo con el nombre '{data.grupo_cuatro}'")
        return await self.repository.create(data)
    
    async def get_by_id(self, id: UUID) -> Optional[GruposCuatroResponse]:
        """Obtener grupo por ID."""
        return await self.repository.get_by_id(id)
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> GruposCuatroListResponse:
        """Obtener todos los grupos."""
        items = await self.repository.get_all(skip, limit)
        total = await self.repository.count()
        return GruposCuatroListResponse(items=items, total=total)
    
    async def update(self, id: UUID, data: GruposCuatroUpdate) -> Optional[GruposCuatroResponse]:
        """Actualizar un grupo."""
        if data.grupo_cuatro:
            existing = await self.repository.get_by_nombre(data.grupo_cuatro)
            if existing and existing.id != id:
                raise ValueError(f"Ya existe otro grupo con el nombre '{data.grupo_cuatro}'")
        return await self.repository.update(id, data)
    
    async def delete(self, id: UUID) -> bool:
        """Eliminar un grupo."""
        return await self.repository.delete(id)


class GruposCincoUseCase:
    """Casos de uso para Grupos Cinco."""
    
    def __init__(self, repository: GruposCincoRepositoryPort):
        self.repository = repository
    
    async def create(self, data: GruposCincoCreate) -> GruposCincoResponse:
        """Crear un nuevo grupo."""
        existing = await self.repository.get_by_nombre(data.grupo_cinco)
        if existing:
            raise ValueError(f"Ya existe un grupo con el nombre '{data.grupo_cinco}'")
        return await self.repository.create(data)
    
    async def get_by_id(self, id: UUID) -> Optional[GruposCincoResponse]:
        """Obtener grupo por ID."""
        return await self.repository.get_by_id(id)
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> GruposCincoListResponse:
        """Obtener todos los grupos."""
        items = await self.repository.get_all(skip, limit)
        total = await self.repository.count()
        return GruposCincoListResponse(items=items, total=total)
    
    async def update(self, id: UUID, data: GruposCincoUpdate) -> Optional[GruposCincoResponse]:
        """Actualizar un grupo."""
        if data.grupo_cinco:
            existing = await self.repository.get_by_nombre(data.grupo_cinco)
            if existing and existing.id != id:
                raise ValueError(f"Ya existe otro grupo con el nombre '{data.grupo_cinco}'")
        return await self.repository.update(id, data)
    
    async def delete(self, id: UUID) -> bool:
        """Eliminar un grupo."""
        return await self.repository.delete(id)
