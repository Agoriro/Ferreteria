"""
DTOs para DiasEntregaProveedor - Principio SOLID: Interface Segregation.
Diferentes interfaces para diferentes operaciones.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class DiasEntregaProveedorBase(BaseModel):
    """Base schema con campos comunes."""
    empresa: str = Field(..., min_length=1, max_length=100, description="Código o nombre de la empresa")
    nit_proveedor: str = Field(..., min_length=1, max_length=200, description="NIT o identificación del proveedor")
    dias_entrega: int = Field(..., ge=0, description="Cantidad de días estimados de entrega")


class DiasEntregaProveedorCreate(DiasEntregaProveedorBase):
    """DTO para creación de registro."""
    pass


class DiasEntregaProveedorUpdate(BaseModel):
    """DTO para actualización - todos los campos opcionales."""
    empresa: Optional[str] = Field(None, min_length=1, max_length=100)
    nit_proveedor: Optional[str] = Field(None, min_length=1, max_length=200)
    dias_entrega: Optional[int] = Field(None, ge=0)


class DiasEntregaProveedorResponse(DiasEntregaProveedorBase):
    """DTO para respuesta."""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class DiasEntregaProveedorListResponse(BaseModel):
    """DTO para respuesta paginada."""
    items: List[DiasEntregaProveedorResponse]
    total: int
    skip: int
    limit: int


# Schemas para lista desplegable de proveedores
class ProveedorOption(BaseModel):
    """DTO para opción de proveedor en lista desplegable."""
    nit_proveedor: str = Field(..., description="NIT del proveedor")
    nombre_proveedor: str = Field(..., description="Nombre del proveedor")
    
    model_config = ConfigDict(from_attributes=True)


class ProveedorOptionsResponse(BaseModel):
    """DTO para lista de opciones de proveedores."""
    items: List[ProveedorOption]
    total: int
