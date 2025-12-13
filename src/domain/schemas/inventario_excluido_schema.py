"""
DTOs para InventarioExcluido - Principio SOLID: Interface Segregation.
Diferentes interfaces para diferentes operaciones.
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID


class InventarioExcluidoBase(BaseModel):
    """Base schema con campos comunes."""
    codigo_producto: str = Field(..., min_length=1, max_length=100, description="Código del producto a excluir")


class InventarioExcluidoCreate(InventarioExcluidoBase):
    """DTO para creación de registro."""
    status: bool = Field(default=True, description="Estado del registro (activo/inactivo)")


class InventarioExcluidoUpdate(BaseModel):
    """DTO para actualización - todos los campos opcionales."""
    codigo_producto: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[bool] = None


class InventarioExcluidoToggleStatus(BaseModel):
    """DTO para cambiar el estado."""
    status: bool = Field(..., description="Nuevo estado del registro")


class InventarioExcluidoResponse(InventarioExcluidoBase):
    """DTO para respuesta."""
    id: UUID
    status: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class InventarioExcluidoListResponse(BaseModel):
    """DTO para respuesta paginada."""
    items: list[InventarioExcluidoResponse]
    total: int
    skip: int
    limit: int

