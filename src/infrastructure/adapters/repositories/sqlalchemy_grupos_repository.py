"""
Implementación SQLAlchemy de los repositorios de Grupos.
"""
from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from domain.ports.grupos_repository import (
    GruposTresRepositoryPort,
    GruposCuatroRepositoryPort,
    GruposCincoRepositoryPort
)
from domain.schemas.grupos_schema import (
    GruposTresCreate, GruposTresUpdate, GruposTresResponse,
    GruposCuatroCreate, GruposCuatroUpdate, GruposCuatroResponse,
    GruposCincoCreate, GruposCincoUpdate, GruposCincoResponse
)
from infrastructure.models.sqlalchemy_models import (
    GruposTresModel,
    GruposCuatroModel,
    GruposCincoModel
)


class SQLAlchemyGruposTresRepository(GruposTresRepositoryPort):
    """Implementación SQLAlchemy del repositorio de Grupos Tres."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def _model_to_response(self, model: GruposTresModel) -> GruposTresResponse:
        return GruposTresResponse(
            id=model.id,
            grupo_tres=model.grupo_tres,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    async def create(self, data: GruposTresCreate) -> GruposTresResponse:
        model = GruposTresModel(grupo_tres=data.grupo_tres)
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return self._model_to_response(model)
    
    async def get_by_id(self, id: UUID) -> Optional[GruposTresResponse]:
        result = await self.db.execute(
            select(GruposTresModel).where(GruposTresModel.id == id)
        )
        model = result.scalar_one_or_none()
        return self._model_to_response(model) if model else None
    
    async def get_by_nombre(self, nombre: str) -> Optional[GruposTresResponse]:
        result = await self.db.execute(
            select(GruposTresModel).where(GruposTresModel.grupo_tres == nombre)
        )
        model = result.scalar_one_or_none()
        return self._model_to_response(model) if model else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[GruposTresResponse]:
        result = await self.db.execute(
            select(GruposTresModel)
            .order_by(GruposTresModel.grupo_tres)
            .offset(skip)
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._model_to_response(m) for m in models]
    
    async def count(self) -> int:
        result = await self.db.execute(
            select(func.count(GruposTresModel.id))
        )
        return result.scalar() or 0
    
    async def update(self, id: UUID, data: GruposTresUpdate) -> Optional[GruposTresResponse]:
        result = await self.db.execute(
            select(GruposTresModel).where(GruposTresModel.id == id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        
        if data.grupo_tres is not None:
            model.grupo_tres = data.grupo_tres
        
        await self.db.commit()
        await self.db.refresh(model)
        return self._model_to_response(model)
    
    async def delete(self, id: UUID) -> bool:
        result = await self.db.execute(
            select(GruposTresModel).where(GruposTresModel.id == id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return False
        
        await self.db.delete(model)
        await self.db.commit()
        return True


class SQLAlchemyGruposCuatroRepository(GruposCuatroRepositoryPort):
    """Implementación SQLAlchemy del repositorio de Grupos Cuatro."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def _model_to_response(self, model: GruposCuatroModel) -> GruposCuatroResponse:
        return GruposCuatroResponse(
            id=model.id,
            grupo_cuatro=model.grupo_cuatro,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    async def create(self, data: GruposCuatroCreate) -> GruposCuatroResponse:
        model = GruposCuatroModel(grupo_cuatro=data.grupo_cuatro)
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return self._model_to_response(model)
    
    async def get_by_id(self, id: UUID) -> Optional[GruposCuatroResponse]:
        result = await self.db.execute(
            select(GruposCuatroModel).where(GruposCuatroModel.id == id)
        )
        model = result.scalar_one_or_none()
        return self._model_to_response(model) if model else None
    
    async def get_by_nombre(self, nombre: str) -> Optional[GruposCuatroResponse]:
        result = await self.db.execute(
            select(GruposCuatroModel).where(GruposCuatroModel.grupo_cuatro == nombre)
        )
        model = result.scalar_one_or_none()
        return self._model_to_response(model) if model else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[GruposCuatroResponse]:
        result = await self.db.execute(
            select(GruposCuatroModel)
            .order_by(GruposCuatroModel.grupo_cuatro)
            .offset(skip)
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._model_to_response(m) for m in models]
    
    async def count(self) -> int:
        result = await self.db.execute(
            select(func.count(GruposCuatroModel.id))
        )
        return result.scalar() or 0
    
    async def update(self, id: UUID, data: GruposCuatroUpdate) -> Optional[GruposCuatroResponse]:
        result = await self.db.execute(
            select(GruposCuatroModel).where(GruposCuatroModel.id == id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        
        if data.grupo_cuatro is not None:
            model.grupo_cuatro = data.grupo_cuatro
        
        await self.db.commit()
        await self.db.refresh(model)
        return self._model_to_response(model)
    
    async def delete(self, id: UUID) -> bool:
        result = await self.db.execute(
            select(GruposCuatroModel).where(GruposCuatroModel.id == id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return False
        
        await self.db.delete(model)
        await self.db.commit()
        return True


class SQLAlchemyGruposCincoRepository(GruposCincoRepositoryPort):
    """Implementación SQLAlchemy del repositorio de Grupos Cinco."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def _model_to_response(self, model: GruposCincoModel) -> GruposCincoResponse:
        return GruposCincoResponse(
            id=model.id,
            grupo_cinco=model.grupo_cinco,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    async def create(self, data: GruposCincoCreate) -> GruposCincoResponse:
        model = GruposCincoModel(grupo_cinco=data.grupo_cinco)
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return self._model_to_response(model)
    
    async def get_by_id(self, id: UUID) -> Optional[GruposCincoResponse]:
        result = await self.db.execute(
            select(GruposCincoModel).where(GruposCincoModel.id == id)
        )
        model = result.scalar_one_or_none()
        return self._model_to_response(model) if model else None
    
    async def get_by_nombre(self, nombre: str) -> Optional[GruposCincoResponse]:
        result = await self.db.execute(
            select(GruposCincoModel).where(GruposCincoModel.grupo_cinco == nombre)
        )
        model = result.scalar_one_or_none()
        return self._model_to_response(model) if model else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[GruposCincoResponse]:
        result = await self.db.execute(
            select(GruposCincoModel)
            .order_by(GruposCincoModel.grupo_cinco)
            .offset(skip)
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._model_to_response(m) for m in models]
    
    async def count(self) -> int:
        result = await self.db.execute(
            select(func.count(GruposCincoModel.id))
        )
        return result.scalar() or 0
    
    async def update(self, id: UUID, data: GruposCincoUpdate) -> Optional[GruposCincoResponse]:
        result = await self.db.execute(
            select(GruposCincoModel).where(GruposCincoModel.id == id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        
        if data.grupo_cinco is not None:
            model.grupo_cinco = data.grupo_cinco
        
        await self.db.commit()
        await self.db.refresh(model)
        return self._model_to_response(model)
    
    async def delete(self, id: UUID) -> bool:
        result = await self.db.execute(
            select(GruposCincoModel).where(GruposCincoModel.id == id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return False
        
        await self.db.delete(model)
        await self.db.commit()
        return True
