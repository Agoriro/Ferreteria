"""
DTOs para Vista_Tabla_Inventarios - Principio SOLID: Interface Segregation.
Esquemas específicos para listar productos del inventario.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID


class VistaInventarioItem(BaseModel):
    """DTO para respuesta de un item de inventario (campos básicos)."""
    empresa: str = Field(..., description="Empresa a la que pertenece el producto")
    codigo_producto: str = Field(..., description="Código único del producto")
    descripcion: Optional[str] = Field(None, description="Descripción del producto")
    
    model_config = ConfigDict(from_attributes=True)


class VistaInventariosListResponse(BaseModel):
    """DTO para respuesta paginada de inventarios."""
    items: list[VistaInventarioItem]
    total: int
    skip: int
    limit: int

