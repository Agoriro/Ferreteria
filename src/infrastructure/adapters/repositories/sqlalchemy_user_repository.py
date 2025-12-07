"""
Implementación concreta del repositorio de usuarios (Adaptador).
Principio SOLID: Liskov Substitution - Puede reemplazar la abstracción.
"""
from typing import List, Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.ports.user_repository import UserRepositoryPort
from domain.schemas.user_schema import UserCreate, UserUpdate
from infrastructure.models.sqlalchemy_models import UserModel


class SQLAlchemyUserRepository(UserRepositoryPort):
    """Adaptador de persistencia para usuarios usando SQLAlchemy."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, user_data: UserCreate, hashed_password: str) -> UserModel:
        """Crea un nuevo usuario."""
        db_user = UserModel(
            username=user_data.username,
            password=hashed_password,
            nombres=user_data.nombres,
            apellidos=user_data.apellidos,
            id_proveedor=user_data.id_proveedor,
            rol_id=user_data.rol_id,
        )
        
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user
    
    async def get_by_id(self, user_id: int) -> Optional[UserModel]:
        """Obtiene usuario por ID con su rol."""
        stmt = select(UserModel).options(selectinload(UserModel.rol)).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[UserModel]:
        """Obtiene usuario por username."""
        stmt = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100, include_inactive: bool = False) -> List[UserModel]:
        """Lista usuarios."""
        stmt = select(UserModel).options(selectinload(UserModel.rol))
        
        if not include_inactive:
            stmt = stmt.where(UserModel.estado == True)
        
        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[UserModel]:
        """Actualiza usuario."""
        update_data = user_data.model_dump(exclude_unset=True)
        
        if update_data:
            stmt = (
                update(UserModel)
                .where(UserModel.id == user_id)
                .values(**update_data)
                .returning(UserModel)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one_or_none()
        
        return await self.get_by_id(user_id)
    
    async def soft_delete(self, user_id: int) -> bool:
        """Soft delete (cambiar estado)."""
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(estado=False)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0
    
    async def update_password(self, user_id: int, hashed_password: str) -> bool:
        """Actualiza contraseña."""
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(password=hashed_password)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0
