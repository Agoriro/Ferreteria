"""
Implementación del repositorio de roles.
"""
from typing import List, Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from domain.ports.role_repository import RoleRepositoryPort
from domain.schemas.role_schema import RoleCreate, RoleUpdate
from infrastructure.models.sqlalchemy_models import RoleModel


class SQLAlchemyRoleRepository(RoleRepositoryPort):
    """Adaptador de persistencia para roles."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, role_data: RoleCreate) -> RoleModel:
        """Crea un nuevo rol."""
        db_role = RoleModel(
            nombre_rol=role_data.nombre_rol,
            descripcion=role_data.descripcion
        )
        
        self.session.add(db_role)
        await self.session.commit()
        await self.session.refresh(db_role)
        return db_role
    
    async def get_by_id(self, role_id: int) -> Optional[RoleModel]:
        """Obtiene rol por ID."""
        stmt = select(RoleModel).where(RoleModel.id_rol == role_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_name(self, nombre_rol: str) -> Optional[RoleModel]:
        """Obtiene rol por nombre."""
        stmt = select(RoleModel).where(RoleModel.nombre_rol == nombre_rol)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all(self) -> List[RoleModel]:
        """Lista todos los roles."""
        stmt = select(RoleModel)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def update(self, role_id: int, role_data: RoleUpdate) -> Optional[RoleModel]:
        """Actualiza un rol."""
        update_data = role_data.model_dump(exclude_unset=True)
        
        if update_data:
            stmt = (
                update(RoleModel)
                .where(RoleModel.id_rol == role_id)
                .values(**update_data)
                .returning(RoleModel)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one_or_none()
        
        return await self.get_by_id(role_id)
