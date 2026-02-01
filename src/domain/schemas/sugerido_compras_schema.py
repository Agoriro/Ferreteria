"""
Schemas Pydantic para Sugerido de Compras.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID
from enum import Enum
from decimal import Decimal


class StatusSugerido(str, Enum):
    """Enum para el status de sugerido de compras."""
    Created = "Created"
    Requested = "Requested"
    Processed = "Processed"


class SugeridoComprasBase(BaseModel):
    """Schema base para Sugerido de Compras."""
    empresa: str = Field(..., max_length=100)
    fecha: Optional[date] = None
    num_doc: Optional[str] = Field(None, max_length=100)
    proveedor: Optional[str] = Field(None, max_length=255)
    grupo3: Optional[str] = Field(None, max_length=255)
    grupo4: Optional[str] = Field(None, max_length=255)
    grupo5: Optional[str] = Field(None, max_length=255)
    cod_prod: str = Field(..., max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    unidad_medida: Optional[str] = Field(None, max_length=50)
    exist: Optional[Decimal] = Field(default=Decimal("0"))
    exist_mc: Optional[Decimal] = Field(default=Decimal("0"))
    cantidad_ventas_anterior: Optional[Decimal] = Field(default=Decimal("0"))
    cantidad_ventas_actual: Optional[Decimal] = Field(default=Decimal("0"))
    sugerido_compras: Optional[Decimal] = Field(default=Decimal("0"))
    cantidad_a_pedir: Optional[Decimal] = Field(default=Decimal("0"))
    proveedor1: Optional[str] = Field(None, max_length=255)
    proveedor2: Optional[str] = Field(None, max_length=255)
    proveedor3: Optional[str] = Field(None, max_length=255)
    proveedor4: Optional[str] = Field(None, max_length=255)
    compras_en_el_periodo: Optional[Decimal] = Field(default=Decimal("0"))
    total_entradas_en_el_periodo: Optional[Decimal] = Field(default=Decimal("0"))
    ultima_fecha_compra: Optional[date] = None
    ventas_en_el_periodo: Optional[Decimal] = Field(default=Decimal("0"))
    total_salidas_en_el_periodo: Optional[Decimal] = Field(default=Decimal("0"))
    ultima_fecha_venta: Optional[date] = None
    saldo_actual: Optional[Decimal] = Field(default=Decimal("0"))
    val_unit: Optional[Decimal] = Field(default=Decimal("0"))
    dcto: Optional[Decimal] = Field(default=Decimal("0"))
    val_neto: Optional[Decimal] = Field(default=Decimal("0"))
    precio1: Optional[Decimal] = Field(default=Decimal("0"))
    util_1: Optional[Decimal] = Field(default=Decimal("0"))
    precio2: Optional[Decimal] = Field(default=Decimal("0"))
    util_2: Optional[Decimal] = Field(default=Decimal("0"))
    status: StatusSugerido = StatusSugerido.Created


class SugeridoComprasCreate(SugeridoComprasBase):
    """Schema para crear Sugerido de Compras."""
    pass


class SugeridoComprasUpdate(BaseModel):
    """Schema para actualizar Sugerido de Compras."""
    empresa: Optional[str] = Field(None, max_length=100)
    fecha: Optional[date] = None
    num_doc: Optional[str] = Field(None, max_length=100)
    proveedor: Optional[str] = Field(None, max_length=255)
    grupo3: Optional[str] = Field(None, max_length=255)
    grupo4: Optional[str] = Field(None, max_length=255)
    grupo5: Optional[str] = Field(None, max_length=255)
    cod_prod: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    unidad_medida: Optional[str] = Field(None, max_length=50)
    exist: Optional[Decimal] = None
    exist_mc: Optional[Decimal] = None
    cantidad_ventas_anterior: Optional[Decimal] = None
    cantidad_ventas_actual: Optional[Decimal] = None
    sugerido_compras: Optional[Decimal] = None
    cantidad_a_pedir: Optional[Decimal] = None
    proveedor1: Optional[str] = Field(None, max_length=255)
    proveedor2: Optional[str] = Field(None, max_length=255)
    proveedor3: Optional[str] = Field(None, max_length=255)
    proveedor4: Optional[str] = Field(None, max_length=255)
    compras_en_el_periodo: Optional[Decimal] = None
    total_entradas_en_el_periodo: Optional[Decimal] = None
    ultima_fecha_compra: Optional[date] = None
    ventas_en_el_periodo: Optional[Decimal] = None
    total_salidas_en_el_periodo: Optional[Decimal] = None
    ultima_fecha_venta: Optional[date] = None
    saldo_actual: Optional[Decimal] = None
    val_unit: Optional[Decimal] = None
    dcto: Optional[Decimal] = None
    val_neto: Optional[Decimal] = None
    precio1: Optional[Decimal] = None
    util_1: Optional[Decimal] = None
    precio2: Optional[Decimal] = None
    util_2: Optional[Decimal] = None
    status: Optional[StatusSugerido] = None


class SugeridoComprasStatusUpdate(BaseModel):
    """Schema para actualizar solo el status."""
    status: StatusSugerido


class SugeridoComprasResponse(SugeridoComprasBase):
    """Schema de respuesta para Sugerido de Compras."""
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class SugeridoComprasListResponse(BaseModel):
    """Schema para lista de Sugerido de Compras."""
    items: List[SugeridoComprasResponse]
    total: int


class GenerarSugeridoRequest(BaseModel):
    """Schema para el request de generar sugerido de compras."""
    fecha_inicial: date = Field(..., description="Fecha inicial del periodo")
    fecha_final: date = Field(..., description="Fecha final del periodo")
    grupo3: Optional[str] = Field(None, description="Filtro por Grupo 3")
    grupo4: Optional[str] = Field(None, description="Filtro por Grupo 4")
    grupo5: Optional[str] = Field(None, description="Filtro por Grupo 5")

