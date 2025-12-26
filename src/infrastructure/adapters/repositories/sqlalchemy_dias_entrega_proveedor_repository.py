"""
Implementación concreta del repositorio de días de entrega por proveedor (Adaptador).
Principio SOLID: Liskov Substitution - Puede reemplazar la abstracción.
"""
from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from domain.ports.dias_entrega_proveedor_repository import DiasEntregaProveedorRepositoryPort
from domain.schemas.dias_entrega_proveedor_schema import DiasEntregaProveedorCreate, DiasEntregaProveedorUpdate
from infrastructure.models.sqlalchemy_models import DiasEntregaProveedorModel


class SQLAlchemyDiasEntregaProveedorRepository(DiasEntregaProveedorRepositoryPort):
    """Adaptador de persistencia para días de entrega por proveedor usando SQLAlchemy."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, data: DiasEntregaProveedorCreate) -> DiasEntregaProveedorModel:
        """Crea un nuevo registro de días de entrega."""
        db_record = DiasEntregaProveedorModel(
            empresa=data.empresa,
            nit_proveedor=data.nit_proveedor,
            dias_entrega=data.dias_entrega
        )
        
        self.session.add(db_record)
        await self.session.commit()
        await self.session.refresh(db_record)
        return db_record
    
    async def get_by_id(self, record_id: UUID) -> Optional[DiasEntregaProveedorModel]:
        """Obtiene registro por ID."""
        stmt = select(DiasEntregaProveedorModel).where(DiasEntregaProveedorModel.id == record_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_empresa_nit(self, empresa: str, nit_proveedor: str) -> Optional[DiasEntregaProveedorModel]:
        """Obtiene registro por empresa y NIT del proveedor (combinación única)."""
        stmt = select(DiasEntregaProveedorModel).where(
            DiasEntregaProveedorModel.empresa == empresa,
            DiasEntregaProveedorModel.nit_proveedor == nit_proveedor
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> Tuple[List[DiasEntregaProveedorModel], int]:
        """Lista todos los registros con paginación."""
        # Query base
        base_query = select(DiasEntregaProveedorModel)
        count_query = select(func.count()).select_from(DiasEntregaProveedorModel)
        
        # Obtener total
        total_result = await self.session.execute(count_query)
        total = total_result.scalar()
        
        # Obtener registros paginados
        stmt = base_query.offset(skip).limit(limit).order_by(DiasEntregaProveedorModel.empresa, DiasEntregaProveedorModel.nit_proveedor)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        
        return items, total
    
    async def get_by_empresa(
        self, 
        empresa: str,
        skip: int = 0, 
        limit: int = 100
    ) -> Tuple[List[DiasEntregaProveedorModel], int]:
        """Lista registros filtrados por empresa."""
        # Query base con filtro
        base_query = select(DiasEntregaProveedorModel).where(DiasEntregaProveedorModel.empresa == empresa)
        count_query = select(func.count()).select_from(DiasEntregaProveedorModel).where(DiasEntregaProveedorModel.empresa == empresa)
        
        # Obtener total
        total_result = await self.session.execute(count_query)
        total = total_result.scalar()
        
        # Obtener registros paginados
        stmt = base_query.offset(skip).limit(limit).order_by(DiasEntregaProveedorModel.nit_proveedor)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        
        return items, total
    
    async def update(self, record_id: UUID, data: DiasEntregaProveedorUpdate) -> Optional[DiasEntregaProveedorModel]:
        """Actualiza un registro."""
        update_data = data.model_dump(exclude_unset=True)
        
        if update_data:
            stmt = (
                update(DiasEntregaProveedorModel)
                .where(DiasEntregaProveedorModel.id == record_id)
                .values(**update_data)
                .returning(DiasEntregaProveedorModel)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one_or_none()
        
        return await self.get_by_id(record_id)
    
    async def delete(self, record_id: UUID) -> bool:
        """Elimina un registro permanentemente."""
        stmt = delete(DiasEntregaProveedorModel).where(DiasEntregaProveedorModel.id == record_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0



