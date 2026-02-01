"""
Schemas para listado de proveedores (dropdown).
"""
from pydantic import BaseModel, Field, ConfigDict


class ProveedorDropdownItem(BaseModel):
    """Item para lista desplegable de proveedores (value + label)."""
    identificacion: str = Field(..., description="Identificación del proveedor (valor)")
    nombre_completo: str = Field(..., description="Nombre completo (etiqueta)")

    model_config = ConfigDict(from_attributes=True)
