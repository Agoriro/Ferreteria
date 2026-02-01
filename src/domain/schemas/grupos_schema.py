"""
Schemas Pydantic para Grupos (Tres, Cuatro, Cinco).
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# ============== Grupos Tres ==============

class GruposTresBase(BaseModel):
    """Schema base para Grupos Tres."""
    grupo_tres: str = Field(..., max_length=255, description="Nombre del grupo tres")


class GruposTresCreate(GruposTresBase):
    """Schema para crear un Grupo Tres."""
    pass


class GruposTresUpdate(BaseModel):
    """Schema para actualizar un Grupo Tres."""
    grupo_tres: Optional[str] = Field(None, max_length=255)


class GruposTresResponse(GruposTresBase):
    """Schema de respuesta para Grupo Tres."""
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class GruposTresListResponse(BaseModel):
    """Schema de respuesta para lista de Grupos Tres."""
    items: List[GruposTresResponse]
    total: int


# ============== Grupos Cuatro ==============

class GruposCuatroBase(BaseModel):
    """Schema base para Grupos Cuatro."""
    grupo_cuatro: str = Field(..., max_length=255, description="Nombre del grupo cuatro")


class GruposCuatroCreate(GruposCuatroBase):
    """Schema para crear un Grupo Cuatro."""
    pass


class GruposCuatroUpdate(BaseModel):
    """Schema para actualizar un Grupo Cuatro."""
    grupo_cuatro: Optional[str] = Field(None, max_length=255)


class GruposCuatroResponse(GruposCuatroBase):
    """Schema de respuesta para Grupo Cuatro."""
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class GruposCuatroListResponse(BaseModel):
    """Schema de respuesta para lista de Grupos Cuatro."""
    items: List[GruposCuatroResponse]
    total: int


# ============== Grupos Cinco ==============

class GruposCincoBase(BaseModel):
    """Schema base para Grupos Cinco."""
    grupo_cinco: str = Field(..., max_length=255, description="Nombre del grupo cinco")


class GruposCincoCreate(GruposCincoBase):
    """Schema para crear un Grupo Cinco."""
    pass


class GruposCincoUpdate(BaseModel):
    """Schema para actualizar un Grupo Cinco."""
    grupo_cinco: Optional[str] = Field(None, max_length=255)


class GruposCincoResponse(GruposCincoBase):
    """Schema de respuesta para Grupo Cinco."""
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class GruposCincoListResponse(BaseModel):
    """Schema de respuesta para lista de Grupos Cinco."""
    items: List[GruposCincoResponse]
    total: int


# ============== Respuesta Combinada ==============

class GruposCombinedResponse(BaseModel):
    """Schema de respuesta combinada con todos los grupos."""
    Grupo_Tres: List[str]
    Grupo_Cuatro: List[str]
    Grupo_Cinco: List[str]
