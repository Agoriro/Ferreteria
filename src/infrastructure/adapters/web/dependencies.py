"""
Inyección de dependencias para FastAPI.
Principio SOLID: Dependency Inversion aplicado.
"""
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.config.database import get_db
from infrastructure.security.jwt_handler import JWTHandler
from infrastructure.adapters.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from infrastructure.adapters.repositories.sqlalchemy_role_repository import SQLAlchemyRoleRepository
from infrastructure.adapters.repositories.sqlalchemy_inventario_excluido_repository import SQLAlchemyInventarioExcluidoRepository
from infrastructure.adapters.repositories.sqlalchemy_dias_entrega_proveedor_repository import SQLAlchemyDiasEntregaProveedorRepository
from infrastructure.adapters.repositories.sqlalchemy_vista_inventarios_repository import SQLAlchemyVistaInventariosRepository
from application.use_cases.user_use_case import UserUseCase
from application.use_cases.auth_use_case import AuthUseCase
from application.use_cases.role_use_case import RoleUseCase
from application.use_cases.inventario_excluido_use_case import InventarioExcluidoUseCase
from application.use_cases.dias_entrega_proveedor_use_case import DiasEntregaProveedorUseCase
from application.use_cases.vista_inventarios_use_case import VistaInventariosUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# Repositorios
def get_user_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyUserRepository:
    """Factory para repositorio de usuarios."""
    return SQLAlchemyUserRepository(db)


def get_role_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyRoleRepository:
    """Factory para repositorio de roles."""
    return SQLAlchemyRoleRepository(db)


def get_inventario_excluido_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyInventarioExcluidoRepository:
    """Factory para repositorio de inventario excluido."""
    return SQLAlchemyInventarioExcluidoRepository(db)


def get_dias_entrega_proveedor_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyDiasEntregaProveedorRepository:
    """Factory para repositorio de días de entrega por proveedor."""
    return SQLAlchemyDiasEntregaProveedorRepository(db)


def get_vista_inventarios_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyVistaInventariosRepository:
    """Factory para repositorio de vista de inventarios."""
    return SQLAlchemyVistaInventariosRepository(db)


# JWT Handler
def get_jwt_handler() -> JWTHandler:
    """Factory para JWT handler."""
    return JWTHandler()


# Use Cases
def get_user_use_case(
    user_repo: SQLAlchemyUserRepository = Depends(get_user_repository)
) -> UserUseCase:
    """Factory para caso de uso de usuarios."""
    return UserUseCase(user_repo)


def get_auth_use_case(
    user_repo: SQLAlchemyUserRepository = Depends(get_user_repository),
    jwt_handler: JWTHandler = Depends(get_jwt_handler)
) -> AuthUseCase:
    """Factory para caso de uso de autenticación."""
    return AuthUseCase(user_repo, jwt_handler)


def get_role_use_case(
    role_repo: SQLAlchemyRoleRepository = Depends(get_role_repository)
) -> RoleUseCase:
    """Factory para caso de uso de roles."""
    return RoleUseCase(role_repo)


def get_inventario_excluido_use_case(
    repo: SQLAlchemyInventarioExcluidoRepository = Depends(get_inventario_excluido_repository)
) -> InventarioExcluidoUseCase:
    """Factory para caso de uso de inventario excluido."""
    return InventarioExcluidoUseCase(repo)


def get_dias_entrega_proveedor_use_case(
    repo: SQLAlchemyDiasEntregaProveedorRepository = Depends(get_dias_entrega_proveedor_repository)
) -> DiasEntregaProveedorUseCase:
    """Factory para caso de uso de días de entrega por proveedor."""
    return DiasEntregaProveedorUseCase(repo)


def get_vista_inventarios_use_case(
    repo: SQLAlchemyVistaInventariosRepository = Depends(get_vista_inventarios_repository)
) -> VistaInventariosUseCase:
    """Factory para caso de uso de vista de inventarios."""
    return VistaInventariosUseCase(repo)


# Autenticación
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
    user_repo: SQLAlchemyUserRepository = Depends(get_user_repository)
):
    """Obtiene usuario actual desde token JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = jwt_handler.verify_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    user = await user_repo.get_by_username(username)
    if user is None:
        raise credentials_exception
    
    if not user.estado:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    return user
