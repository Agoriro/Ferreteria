"""
Router para gestión de días de entrega por proveedor.
"""
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status, Query

from domain.schemas.dias_entrega_proveedor_schema import (
    DiasEntregaProveedorCreate,
    DiasEntregaProveedorResponse,
    DiasEntregaProveedorUpdate,
    DiasEntregaProveedorListResponse,
    ProveedorOptionsResponse
)
from application.use_cases.dias_entrega_proveedor_use_case import DiasEntregaProveedorUseCase
from infrastructure.adapters.web.dependencies import (
    get_dias_entrega_proveedor_use_case, 
    get_current_user
)
from infrastructure.models.sqlalchemy_models import UserModel

router = APIRouter(prefix="/dias-entrega-proveedor", tags=["Días Entrega Proveedor"])


# ============================================
# ENDPOINTS PARA DROPDOWNS (LISTAS DESPLEGABLES)
# ============================================

@router.get("/options/proveedores/{empresa}", response_model=ProveedorOptionsResponse)
async def get_proveedores_options(
    empresa: str,
    search: Optional[str] = Query(None, description="Buscar por NIT o nombre"),
    limit: int = Query(50, ge=1, le=200, description="Límite de resultados"),
    use_case: DiasEntregaProveedorUseCase = Depends(get_dias_entrega_proveedor_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Obtiene lista de proveedores para lista desplegable (dropdown).
    
    Retorna NIT y nombre del proveedor filtrados por empresa.
    
    - **empresa**: Código de la empresa para filtrar proveedores
    - **search**: Texto para buscar por NIT o nombre (opcional)
    - **limit**: Número máximo de resultados (default: 50)
    """
    return await use_case.get_proveedores_options(empresa, search, limit)


# ============================================
# ENDPOINTS CRUD
# ============================================

@router.post("/", response_model=DiasEntregaProveedorResponse, status_code=status.HTTP_201_CREATED)
async def create_dias_entrega_proveedor(
    data: DiasEntregaProveedorCreate,
    use_case: DiasEntregaProveedorUseCase = Depends(get_dias_entrega_proveedor_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Crea un nuevo registro de días de entrega por proveedor.
    
    - **empresa**: Código o nombre de la empresa (requerido)
    - **nit_proveedor**: NIT o identificación del proveedor (requerido)
    - **dias_entrega**: Cantidad de días estimados de entrega (requerido)
    """
    return await use_case.create(data)


@router.get("/", response_model=DiasEntregaProveedorListResponse)
async def list_dias_entrega_proveedor(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros"),
    empresa: Optional[str] = Query(None, description="Filtrar por empresa"),
    use_case: DiasEntregaProveedorUseCase = Depends(get_dias_entrega_proveedor_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Lista todos los registros de días de entrega por proveedor.
    
    - **skip**: Número de registros a saltar (paginación)
    - **limit**: Número máximo de registros a retornar
    - **empresa**: Filtrar por empresa (opcional)
    """
    return await use_case.get_all(skip, limit, empresa)


@router.get("/{record_id}", response_model=DiasEntregaProveedorResponse)
async def get_dias_entrega_proveedor(
    record_id: UUID,
    use_case: DiasEntregaProveedorUseCase = Depends(get_dias_entrega_proveedor_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Obtiene un registro de días de entrega por ID.
    
    - **record_id**: UUID del registro a buscar
    """
    return await use_case.get_by_id(record_id)


@router.patch("/{record_id}", response_model=DiasEntregaProveedorResponse)
async def update_dias_entrega_proveedor(
    record_id: UUID,
    data: DiasEntregaProveedorUpdate,
    use_case: DiasEntregaProveedorUseCase = Depends(get_dias_entrega_proveedor_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Actualiza un registro de días de entrega.
    
    - **record_id**: UUID del registro a actualizar
    - **empresa**: Nueva empresa (opcional)
    - **nit_proveedor**: Nuevo NIT del proveedor (opcional)
    - **dias_entrega**: Nueva cantidad de días de entrega (opcional)
    """
    return await use_case.update(record_id, data)


@router.delete("/{record_id}")
async def delete_dias_entrega_proveedor(
    record_id: UUID,
    use_case: DiasEntregaProveedorUseCase = Depends(get_dias_entrega_proveedor_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Elimina permanentemente un registro de días de entrega.
    
    - **record_id**: UUID del registro a eliminar
    """
    return await use_case.delete(record_id)
