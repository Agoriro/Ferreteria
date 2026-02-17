"""
Repositorio SQLAlchemy para Permisos.
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from infrastructure.models.sqlalchemy_models import (
    RoleModel,
    FormularioModel,
    DetallePermisoModel
)


class SQLAlchemyPermisoRepository:
    """Repositorio para operaciones de permisos."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_formularios_by_rol(self, nombre_rol: str) -> List[dict]:
        """
        Obtiene los formularios a los que tiene acceso un rol.
        
        Args:
            nombre_rol: Nombre del rol (ADMIN, COMPRAS, PROVEEDOR)
            
        Returns:
            Lista de formularios con sus permisos
        """
        # Primero, obtener el rol
        rol_query = select(RoleModel).where(RoleModel.nombre_rol == nombre_rol)
        rol_result = await self.db.execute(rol_query)
        rol = rol_result.scalar_one_or_none()
        
        if not rol:
            return []
        
        # Consultar los permisos del rol con los formularios
        query = (
            select(
                FormularioModel.id_formulario,
                FormularioModel.nombre_formulario,
                FormularioModel.descripcion,
                FormularioModel.ruta,
                DetallePermisoModel.puede_leer,
                DetallePermisoModel.puede_crear,
                DetallePermisoModel.puede_editar,
                DetallePermisoModel.puede_eliminar
            )
            .join(
                DetallePermisoModel,
                DetallePermisoModel.id_formulario == FormularioModel.id_formulario
            )
            .where(DetallePermisoModel.id_rol == rol.id_rol)
            .where(DetallePermisoModel.puede_leer == True)
            .order_by(FormularioModel.id_formulario)
        )
        
        result = await self.db.execute(query)
        rows = result.all()
        
        formularios = []
        for row in rows:
            formularios.append({
                "id_formulario": row.id_formulario,
                "nombre_formulario": row.nombre_formulario,
                "descripcion": row.descripcion,
                "ruta": row.ruta,
                "puede_leer": row.puede_leer,
                "puede_crear": row.puede_crear,
                "puede_editar": row.puede_editar,
                "puede_eliminar": row.puede_eliminar
            })
        
        return formularios

    async def get_rol_by_nombre(self, nombre_rol: str) -> Optional[RoleModel]:
        """
        Obtiene un rol por su nombre.
        
        Args:
            nombre_rol: Nombre del rol
            
        Returns:
            RoleModel o None si no existe
        """
        query = select(RoleModel).where(RoleModel.nombre_rol == nombre_rol)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def verificar_permiso(
        self, 
        nombre_rol: str, 
        nombre_formulario: str
    ) -> Optional[dict]:
        """
        Verifica si un rol tiene permiso para acceder a un formulario.
        
        Args:
            nombre_rol: Nombre del rol
            nombre_formulario: Nombre del formulario
            
        Returns:
            Diccionario con los permisos o None si no tiene acceso
        """
        query = (
            select(
                DetallePermisoModel.puede_leer,
                DetallePermisoModel.puede_crear,
                DetallePermisoModel.puede_editar,
                DetallePermisoModel.puede_eliminar
            )
            .join(RoleModel, RoleModel.id_rol == DetallePermisoModel.id_rol)
            .join(FormularioModel, FormularioModel.id_formulario == DetallePermisoModel.id_formulario)
            .where(RoleModel.nombre_rol == nombre_rol)
            .where(FormularioModel.nombre_formulario == nombre_formulario)
        )
        
        result = await self.db.execute(query)
        row = result.first()
        
        if not row:
            return None
        
        return {
            "puede_leer": row.puede_leer,
            "puede_crear": row.puede_crear,
            "puede_editar": row.puede_editar,
            "puede_eliminar": row.puede_eliminar
        }
