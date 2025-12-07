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
from application.use_cases.user_use_case import UserUseCase
from application.use_cases.auth_use_case import AuthUseCase
from application.use_cases.role_use_case import RoleUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# Repositorios
def get_user_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyUserRepository:
    """Factory para repositorio de usuarios."""
    return SQLAlchemyUserRepository(db)


def get_role_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyRoleRepository:
    """Factory para repositorio de roles."""
    return SQLAlchemyRoleRepository(db)


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
