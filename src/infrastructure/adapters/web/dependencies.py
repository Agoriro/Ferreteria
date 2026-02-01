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
from infrastructure.adapters.repositories.sqlalchemy_sugerido_compras_repository import SQLAlchemySugeridoComprasRepository
from infrastructure.adapters.repositories.sqlalchemy_grupos_repository import (
    SQLAlchemyGruposTresRepository,
    SQLAlchemyGruposCuatroRepository,
    SQLAlchemyGruposCincoRepository
)
from infrastructure.adapters.repositories.sqlalchemy_proveedores_repository import SQLAlchemyProveedoresRepository
from infrastructure.adapters.repositories.sqlalchemy_permiso_repository import SQLAlchemyPermisoRepository
from application.use_cases.user_use_case import UserUseCase
from application.use_cases.auth_use_case import AuthUseCase
from application.use_cases.role_use_case import RoleUseCase
from application.use_cases.inventario_excluido_use_case import InventarioExcluidoUseCase
from application.use_cases.dias_entrega_proveedor_use_case import DiasEntregaProveedorUseCase
from application.use_cases.vista_inventarios_use_case import VistaInventariosUseCase
from application.use_cases.sugerido_compras_use_case import SugeridoComprasUseCase
from application.use_cases.grupos_use_case import (
    GruposTresUseCase,
    GruposCuatroUseCase,
    GruposCincoUseCase
)
from application.use_cases.proveedores_use_case import ProveedoresUseCase
from application.use_cases.permiso_use_case import PermisoUseCase

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


def get_sugerido_compras_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemySugeridoComprasRepository:
    """Factory para repositorio de sugerido de compras."""
    return SQLAlchemySugeridoComprasRepository(db)


def get_sugerido_compras_use_case(
    repo: SQLAlchemySugeridoComprasRepository = Depends(get_sugerido_compras_repository)
) -> SugeridoComprasUseCase:
    """Factory para caso de uso de sugerido de compras."""
    return SugeridoComprasUseCase(repo)


# Grupos Tres
def get_grupos_tres_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyGruposTresRepository:
    """Factory para repositorio de Grupos Tres."""
    return SQLAlchemyGruposTresRepository(db)


def get_grupos_tres_use_case(
    repo: SQLAlchemyGruposTresRepository = Depends(get_grupos_tres_repository)
) -> GruposTresUseCase:
    """Factory para caso de uso de Grupos Tres."""
    return GruposTresUseCase(repo)


# Grupos Cuatro
def get_grupos_cuatro_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyGruposCuatroRepository:
    """Factory para repositorio de Grupos Cuatro."""
    return SQLAlchemyGruposCuatroRepository(db)


def get_grupos_cuatro_use_case(
    repo: SQLAlchemyGruposCuatroRepository = Depends(get_grupos_cuatro_repository)
) -> GruposCuatroUseCase:
    """Factory para caso de uso de Grupos Cuatro."""
    return GruposCuatroUseCase(repo)


# Grupos Cinco
def get_grupos_cinco_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyGruposCincoRepository:
    """Factory para repositorio de Grupos Cinco."""
    return SQLAlchemyGruposCincoRepository(db)


def get_grupos_cinco_use_case(
    repo: SQLAlchemyGruposCincoRepository = Depends(get_grupos_cinco_repository)
) -> GruposCincoUseCase:
    """Factory para caso de uso de Grupos Cinco."""
    return GruposCincoUseCase(repo)


# Proveedores (dropdown)
def get_proveedores_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyProveedoresRepository:
    """Factory para repositorio de proveedores."""
    return SQLAlchemyProveedoresRepository(db)


def get_proveedores_use_case(
    repo: SQLAlchemyProveedoresRepository = Depends(get_proveedores_repository)
) -> ProveedoresUseCase:
    """Factory para caso de uso de proveedores."""
    return ProveedoresUseCase(repo)


# Permisos
def get_permiso_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyPermisoRepository:
    """Factory para repositorio de permisos."""
    return SQLAlchemyPermisoRepository(db)


def get_permiso_use_case(
    repo: SQLAlchemyPermisoRepository = Depends(get_permiso_repository)
) -> PermisoUseCase:
    """Factory para caso de uso de permisos."""
    return PermisoUseCase(repo)


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
