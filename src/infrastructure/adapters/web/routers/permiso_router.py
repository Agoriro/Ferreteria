"""
Router para gestión de permisos.
"""
from fastapi import APIRouter, Depends, HTTPException, status

from domain.schemas.form_schema import PermisosRolResponse
from application.use_cases.permiso_use_case import PermisoUseCase
from infrastructure.adapters.web.dependencies import get_permiso_use_case, get_current_user
from infrastructure.models.sqlalchemy_models import UserModel

router = APIRouter(prefix="/permisos", tags=["Permisos"])


@router.get(
    "/formularios/{nombre_rol}",
    response_model=PermisosRolResponse,
    summary="Obtener formularios permitidos por rol",
    description="""
    Obtiene la lista de formularios a los que tiene acceso un rol específico.
    
    **Roles disponibles:**
    - ADMIN: Acceso a todos los formularios
    - COMPRAS: Acceso a Sugerido de compras, Requisición de compras, Exportar Requisiciones, Reportes
    - PROVEEDOR: Acceso solo a Requisición de compras
    
    **Respuesta:**
    - Lista de formularios con nombre, descripción, ruta y permisos (leer, crear, editar, eliminar)
    """
)
async def get_formularios_by_rol(
    nombre_rol: str,
    permiso_use_case: PermisoUseCase = Depends(get_permiso_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Obtiene los formularios permitidos para un rol.
    
    - **nombre_rol**: Nombre del rol (ADMIN, COMPRAS, PROVEEDOR)
    """
    result = await permiso_use_case.obtener_formularios_permitidos(nombre_rol)
    return result


@router.get(
    "/verificar/{nombre_rol}/{nombre_formulario}",
    summary="Verificar acceso a formulario",
    description="Verifica si un rol tiene acceso a un formulario específico."
)
async def verificar_acceso(
    nombre_rol: str,
    nombre_formulario: str,
    permiso_use_case: PermisoUseCase = Depends(get_permiso_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Verifica si un rol tiene acceso a un formulario.
    
    - **nombre_rol**: Nombre del rol
    - **nombre_formulario**: Nombre del formulario
    """
    result = await permiso_use_case.verificar_acceso(nombre_rol, nombre_formulario)
    return result
