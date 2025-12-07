"""
Router para gestión de roles.
"""
from typing import List
from fastapi import APIRouter, Depends, status

from domain.schemas.role_schema import RoleCreate, RoleResponse, RoleUpdate
from application.use_cases.role_use_case import RoleUseCase
from infrastructure.adapters.web.dependencies import get_role_use_case, get_current_user
from infrastructure.models.sqlalchemy_models import UserModel

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    role_use_case: RoleUseCase = Depends(get_role_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """Crea un nuevo rol."""
    return await role_use_case.create_role(role_data)


@router.get("/", response_model=List[RoleResponse])
async def list_roles(
    role_use_case: RoleUseCase = Depends(get_role_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """Lista todos los roles."""
    return await role_use_case.get_all_roles()


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int,
    role_use_case: RoleUseCase = Depends(get_role_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """Obtiene un rol por ID."""
    return await role_use_case.get_role_by_id(role_id)


@router.patch("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_data: RoleUpdate,
    role_use_case: RoleUseCase = Depends(get_role_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """Actualiza un rol."""
    return await role_use_case.update_role(role_id, role_data)
