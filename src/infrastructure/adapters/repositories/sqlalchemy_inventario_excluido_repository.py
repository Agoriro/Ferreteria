"""
Implementación concreta del repositorio de inventario excluido (Adaptador).
Principio SOLID: Liskov Substitution - Puede reemplazar la abstracción.
"""
from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from domain.ports.inventario_excluido_repository import InventarioExcluidoRepositoryPort
from domain.schemas.inventario_excluido_schema import InventarioExcluidoCreate, InventarioExcluidoUpdate
from infrastructure.models.sqlalchemy_models import InventarioExcluidoModel


class SQLAlchemyInventarioExcluidoRepository(InventarioExcluidoRepositoryPort):
    """Adaptador de persistencia para inventario excluido usando SQLAlchemy."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, data: InventarioExcluidoCreate) -> InventarioExcluidoModel:
        """Crea un nuevo registro de inventario excluido."""
        db_record = InventarioExcluidoModel(
            codigo_producto=data.codigo_producto,
            status=data.status
        )
        
        self.session.add(db_record)
        await self.session.commit()
        await self.session.refresh(db_record)
        return db_record
    
    async def get_by_id(self, record_id: UUID) -> Optional[InventarioExcluidoModel]:
        """Obtiene registro por ID."""
        stmt = select(InventarioExcluidoModel).where(InventarioExcluidoModel.id == record_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_codigo_producto(self, codigo_producto: str) -> Optional[InventarioExcluidoModel]:
        """Obtiene registro por código de producto."""
        stmt = select(InventarioExcluidoModel).where(
            InventarioExcluidoModel.codigo_producto == codigo_producto
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        include_inactive: bool = False
    ) -> Tuple[List[InventarioExcluidoModel], int]:
        """Lista todos los registros con paginación."""
        # Query base
        base_query = select(InventarioExcluidoModel)
        count_query = select(func.count()).select_from(InventarioExcluidoModel)
        
        if not include_inactive:
            base_query = base_query.where(InventarioExcluidoModel.status == True)
            count_query = count_query.where(InventarioExcluidoModel.status == True)
        
        # Obtener total
        total_result = await self.session.execute(count_query)
        total = total_result.scalar()
        
        # Obtener registros paginados
        stmt = base_query.offset(skip).limit(limit).order_by(InventarioExcluidoModel.created_at.desc())
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        
        return items, total
    
    async def update(self, record_id: UUID, data: InventarioExcluidoUpdate) -> Optional[InventarioExcluidoModel]:
        """Actualiza un registro."""
        update_data = data.model_dump(exclude_unset=True)
        
        if update_data:
            stmt = (
                update(InventarioExcluidoModel)
                .where(InventarioExcluidoModel.id == record_id)
                .values(**update_data)
                .returning(InventarioExcluidoModel)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one_or_none()
        
        return await self.get_by_id(record_id)
    
    async def toggle_status(self, record_id: UUID, new_status: bool) -> bool:
        """Cambia el estado de un registro (activo/inactivo)."""
        stmt = (
            update(InventarioExcluidoModel)
            .where(InventarioExcluidoModel.id == record_id)
            .values(status=new_status)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0
    
    async def delete(self, record_id: UUID) -> bool:
        """Elimina un registro permanentemente."""
        stmt = delete(InventarioExcluidoModel).where(InventarioExcluidoModel.id == record_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

