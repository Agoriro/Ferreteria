"""
Router para consulta de inventarios (Vista_Tabla_Inventarios).
"""
from typing import Optional
from fastapi import APIRouter, Depends

from domain.schemas.vista_inventarios_schema import VistaInventariosListResponse
from application.use_cases.vista_inventarios_use_case import VistaInventariosUseCase
from infrastructure.adapters.web.dependencies import (
    get_vista_inventarios_use_case, 
    get_current_user
)
from infrastructure.models.sqlalchemy_models import UserModel

router = APIRouter(prefix="/vista-inventarios", tags=["Vista Inventarios"])


@router.get("/", response_model=VistaInventariosListResponse)
async def list_inventarios(
    skip: int = 0,
    limit: int = 100,
    empresa: Optional[str] = None,
    use_case: VistaInventariosUseCase = Depends(get_vista_inventarios_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Lista todos los productos del inventario con campos básicos.
    
    Retorna: empresa, codigo_producto, descripcion
    
    - **skip**: Número de registros a saltar (paginación)
    - **limit**: Número máximo de registros a retornar
    - **empresa**: Filtro opcional por empresa
    """
    return await use_case.get_all_basic(skip, limit, empresa)

