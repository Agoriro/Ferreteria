"""
Router para gestión de inventario excluido.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, status

from domain.schemas.inventario_excluido_schema import (
    InventarioExcluidoCreate,
    InventarioExcluidoResponse,
    InventarioExcluidoUpdate,
    InventarioExcluidoToggleStatus,
    InventarioExcluidoListResponse
)
from application.use_cases.inventario_excluido_use_case import InventarioExcluidoUseCase
from infrastructure.adapters.web.dependencies import (
    get_inventario_excluido_use_case, 
    get_current_user
)
from infrastructure.models.sqlalchemy_models import UserModel

router = APIRouter(prefix="/inventario-excluido", tags=["Inventario Excluido"])


@router.post("/", response_model=InventarioExcluidoResponse, status_code=status.HTTP_201_CREATED)
async def create_inventario_excluido(
    data: InventarioExcluidoCreate,
    use_case: InventarioExcluidoUseCase = Depends(get_inventario_excluido_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Crea un nuevo registro de inventario excluido.
    
    - **codigo_producto**: Código del producto a excluir (requerido)
    - **status**: Estado del registro, por defecto True (activo)
    """
    return await use_case.create(data)


@router.get("/", response_model=InventarioExcluidoListResponse)
async def list_inventario_excluido(
    skip: int = 0,
    limit: int = 100,
    include_inactive: bool = False,
    use_case: InventarioExcluidoUseCase = Depends(get_inventario_excluido_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Lista todos los registros de inventario excluido.
    
    - **skip**: Número de registros a saltar (paginación)
    - **limit**: Número máximo de registros a retornar
    - **include_inactive**: Incluir registros inactivos
    """
    return await use_case.get_all(skip, limit, include_inactive)


@router.get("/{record_id}", response_model=InventarioExcluidoResponse)
async def get_inventario_excluido(
    record_id: UUID,
    use_case: InventarioExcluidoUseCase = Depends(get_inventario_excluido_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Obtiene un registro de inventario excluido por ID.
    
    - **record_id**: UUID del registro a buscar
    """
    return await use_case.get_by_id(record_id)


@router.patch("/{record_id}", response_model=InventarioExcluidoResponse)
async def update_inventario_excluido(
    record_id: UUID,
    data: InventarioExcluidoUpdate,
    use_case: InventarioExcluidoUseCase = Depends(get_inventario_excluido_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Actualiza un registro de inventario excluido.
    
    - **record_id**: UUID del registro a actualizar
    - **codigo_producto**: Nuevo código del producto (opcional)
    - **status**: Nuevo estado del registro (opcional)
    """
    return await use_case.update(record_id, data)


@router.patch("/{record_id}/toggle-status", response_model=InventarioExcluidoResponse)
async def toggle_status_inventario_excluido(
    record_id: UUID,
    data: InventarioExcluidoToggleStatus,
    use_case: InventarioExcluidoUseCase = Depends(get_inventario_excluido_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Cambia el estado de un registro (activo/inactivo).
    
    - **record_id**: UUID del registro
    - **status**: Nuevo estado (true=activo, false=inactivo)
    """
    return await use_case.toggle_status(record_id, data.status)


@router.delete("/{record_id}")
async def delete_inventario_excluido(
    record_id: UUID,
    use_case: InventarioExcluidoUseCase = Depends(get_inventario_excluido_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Elimina permanentemente un registro de inventario excluido.
    
    - **record_id**: UUID del registro a eliminar
    """
    return await use_case.delete(record_id)

