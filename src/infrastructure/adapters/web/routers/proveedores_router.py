"""
Router para endpoints de proveedores (dropdown).
"""
from fastapi import APIRouter, Depends

from domain.schemas.proveedores_schema import ProveedorDropdownItem
from application.use_cases.proveedores_use_case import ProveedoresUseCase
from infrastructure.adapters.web.dependencies import (
    get_proveedores_use_case,
    get_current_user,
)
from infrastructure.models.sqlalchemy_models import UserModel

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


@router.get("/dropdown", response_model=list[ProveedorDropdownItem])
async def get_proveedores_dropdown(
    use_case: ProveedoresUseCase = Depends(get_proveedores_use_case),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Lista proveedores para lista desplegable.

    Retorna `identificacion` (valor) y `nombre_completo` (etiqueta)
    desde Vista_Auxiliar_Terceros donde Propiedades contiene 'Proveedor'.
    """
    return await use_case.get_proveedores_dropdown()
