"""
DTOs para Roles y Permisos.
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List


class RoleBase(BaseModel):
    nombre_rol: str = Field(..., min_length=1, max_length=50)
    descripcion: Optional[str] = None


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    nombre_rol: Optional[str] = Field(None, min_length=1, max_length=50)
    descripcion: Optional[str] = None


class RoleResponse(RoleBase):
    id_rol: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class PermisoBase(BaseModel):
    puede_leer: bool = True
    puede_crear: bool = False
    puede_editar: bool = False
    puede_eliminar: bool = False


class PermisoCreate(PermisoBase):
    id_rol: int
    id_formulario: int


class PermisoResponse(PermisoBase):
    id_permiso: int
    id_rol: int
    id_formulario: int
    
    model_config = ConfigDict(from_attributes=True)
