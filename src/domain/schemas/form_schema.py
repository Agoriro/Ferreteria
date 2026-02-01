"""
Schemas para Formularios y Permisos.
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class FormularioBase(BaseModel):
    """Schema base para formularios."""
    nombre_formulario: str = Field(..., max_length=100)
    descripcion: Optional[str] = None
    ruta: Optional[str] = Field(None, max_length=255)


class FormularioCreate(FormularioBase):
    """Schema para crear un formulario."""
    pass


class FormularioResponse(BaseModel):
    """Schema de respuesta para formulario."""
    id_formulario: int
    nombre_formulario: str
    descripcion: Optional[str] = None
    ruta: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FormularioPermisoResponse(BaseModel):
    """Schema de respuesta para formulario con permisos."""
    id_formulario: int
    nombre_formulario: str
    descripcion: Optional[str] = None
    ruta: Optional[str] = None
    puede_leer: bool = True
    puede_crear: bool = False
    puede_editar: bool = False
    puede_eliminar: bool = False

    class Config:
        from_attributes = True


class PermisosRolResponse(BaseModel):
    """Schema de respuesta para permisos de un rol."""
    rol: str
    formularios: List[FormularioPermisoResponse]
