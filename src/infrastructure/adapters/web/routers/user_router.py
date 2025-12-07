"""
Router para gestión de usuarios.
"""
from typing import List
from fastapi import APIRouter, Depends, status

from domain.schemas.user_schema import (
    UserCreate, UserResponse, UserUpdate, UserChangePassword, UserWithRole
)
from application.use_cases.user_use_case import UserUseCase
from infrastructure.adapters.web.dependencies import get_user_use_case, get_current_user
from infrastructure.models.sqlalchemy_models import UserModel

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_use_case: UserUseCase = Depends(get_user_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """Crea un nuevo usuario (requiere autenticación)."""
    return await user_use_case.create_user(user_data)


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    include_inactive: bool = False,
    user_use_case: UserUseCase = Depends(get_user_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """Lista todos los usuarios."""
    return await user_use_case.get_all_users(skip, limit, include_inactive)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: UserModel = Depends(get_current_user)
):
    """Obtiene información del usuario actual."""
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    user_use_case: UserUseCase = Depends(get_user_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """Obtiene un usuario por ID."""
    return await user_use_case.get_user_by_id(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_use_case: UserUseCase = Depends(get_user_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """Actualiza un usuario (incluyendo rol)."""
    return await user_use_case.update_user(user_id, user_data)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    user_use_case: UserUseCase = Depends(get_user_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """Soft delete de usuario."""
    return await user_use_case.delete_user(user_id)


@router.post("/{user_id}/change-password")
async def change_password(
    user_id: int,
    password_data: UserChangePassword,
    user_use_case: UserUseCase = Depends(get_user_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """Cambia la contraseña de un usuario."""
    return await user_use_case.change_password(user_id, password_data)
