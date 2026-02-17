"""
Caso de uso para Permisos.
"""
from typing import List
from infrastructure.adapters.repositories.sqlalchemy_permiso_repository import SQLAlchemyPermisoRepository
from domain.schemas.form_schema import FormularioPermisoResponse, PermisosRolResponse


class PermisoUseCase:
    """Caso de uso para operaciones de permisos."""

    def __init__(self, permiso_repo: SQLAlchemyPermisoRepository):
        self.permiso_repo = permiso_repo

    async def obtener_formularios_permitidos(self, nombre_rol: str) -> PermisosRolResponse:
        """
        Obtiene los formularios a los que tiene acceso un rol.
        
        Args:
            nombre_rol: Nombre del rol (ADMIN, COMPRAS, PROVEEDOR)
            
        Returns:
            PermisosRolResponse con la lista de formularios permitidos
        """
        formularios_data = await self.permiso_repo.get_formularios_by_rol(nombre_rol.upper())
        
        formularios = [
            FormularioPermisoResponse(**f) for f in formularios_data
        ]
        
        return PermisosRolResponse(
            rol=nombre_rol.upper(),
            formularios=formularios
        )

    async def verificar_acceso(
        self, 
        nombre_rol: str, 
        nombre_formulario: str
    ) -> dict:
        """
        Verifica si un rol tiene acceso a un formulario específico.
        
        Args:
            nombre_rol: Nombre del rol
            nombre_formulario: Nombre del formulario
            
        Returns:
            Diccionario con tiene_acceso y los permisos específicos
        """
        permisos = await self.permiso_repo.verificar_permiso(
            nombre_rol.upper(), 
            nombre_formulario
        )
        
        if permisos is None:
            return {
                "tiene_acceso": False,
                "permisos": None
            }
        
        return {
            "tiene_acceso": permisos.get("puede_leer", False),
            "permisos": permisos
        }
