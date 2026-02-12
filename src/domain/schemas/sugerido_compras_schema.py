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
    Exported = "Exported"


class SugeridoComprasBase(BaseModel):
    """Schema base para Sugerido de Compras."""
    empresa: str = Field(..., max_length=100)
    fecha: Optional[date] = None
    num_doc: Optional[str] = Field(None, max_length=100)
    proveedor: Optional[str] = Field(None, max_length=255)
    identificacion_tercero: Optional[str] = Field(None, max_length=100)
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
    cantidad_proveedor: Optional[Decimal] = Field(default=Decimal("0"))
    valor_unitario_proveedor: Optional[Decimal] = Field(default=Decimal("0"))
    tipo_doc_exp: Optional[str] = Field(None, max_length=100)
    prefijo_exp: Optional[str] = Field(None, max_length=100)
    num_doc_exp: Optional[str] = Field(None, max_length=100)
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
    identificacion_tercero: Optional[str] = Field(None, max_length=100)
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
    cantidad_proveedor: Optional[Decimal] = None
    valor_unitario_proveedor: Optional[Decimal] = None
    tipo_doc_exp: Optional[str] = Field(None, max_length=100)
    prefijo_exp: Optional[str] = Field(None, max_length=100)
    num_doc_exp: Optional[str] = Field(None, max_length=100)
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


class SugeridoProveedorItem(BaseModel):
    """Schema para cada item en la actualización masiva de proveedor."""
    id: UUID = Field(..., description="ID del registro a actualizar")
    cantidad_proveedor: Decimal = Field(
        ..., 
        gt=0, 
        description="Cantidad del proveedor (debe ser mayor a 0)"
    )
    valor_unitario_proveedor: Decimal = Field(
        ..., 
        gt=0, 
        description="Valor unitario del proveedor (debe ser mayor a 0)"
    )


class SugeridoBulkUpdateRequest(BaseModel):
    """Schema para actualización masiva de sugeridos con datos del proveedor."""
    items: List[SugeridoProveedorItem] = Field(
        ..., 
        min_length=1, 
        description="Lista de items a actualizar"
    )


class SugeridoBulkUpdateResponse(BaseModel):
    """Schema de respuesta para actualización masiva."""
    message: str
    updated_count: int
    updated_ids: List[str]


class SugeridoProcessedResponse(BaseModel):
    """Schema de respuesta para registros con status Processed (campos reducidos)."""
    id: UUID
    empresa: str
    proveedor: Optional[str] = None
    cod_prod: str
    descripcion: Optional[str] = None
    unidad_medida: Optional[str] = None
    cantidad_proveedor: Optional[Decimal] = None
    valor_unitario_proveedor: Optional[Decimal] = None

    class Config:
        from_attributes = True


class SugeridoProcessedListResponse(BaseModel):
    """Schema para lista de registros Processed."""
    items: List[SugeridoProcessedResponse]
    total: int


class SugeridoBulkExportRequest(BaseModel):
    """Schema para actualización masiva a status Exported."""
    ids: List[UUID] = Field(
        ..., 
        min_length=1, 
        description="Lista de IDs a actualizar a status 'Exported'"
    )


class OrdenCompraDetalle(BaseModel):
    """Schema para el detalle de una orden de compra."""
    producto: str = ""
    bodega: str = ""
    unidad_de_medida: str = ""
    cantidad: Decimal = Decimal("0")
    iva: Decimal = Decimal("0")
    valor_unitario: Decimal = Decimal("0")
    descuento: Decimal = Decimal("0")
    vencimiento: str = ""
    nota: str = ""
    centro_costos: str = ""
    codigo_centro_costos: str = ""
    personalizado_1: str = ""
    personalizado_2: str = ""
    personalizado_3: str = ""
    personalizado_4: str = ""
    personalizado_5: str = ""
    personalizado_6: str = ""
    personalizado_7: str = ""
    personalizado_8: str = ""
    personalizado_9: str = ""
    personalizado_10: str = ""
    personalizado_11: str = ""
    personalizado_12: str = ""
    personalizado_13: str = ""
    personalizado_14: str = ""
    personalizado_15: str = ""


class OrdenCompraEncabezado(BaseModel):
    """Schema para el encabezado de una orden de compra."""
    empresa: str = ""
    tipo_documento: str = ""
    prefijo: str = ""
    documento_numero: str = ""
    fecha: str = ""
    tercero_interno: str = ""
    tercero_externo: str = ""
    prefijo_dto_ext: str = ""
    numero_dto_ext: int = 0
    nota: str = ""
    forma_pago: str = ""
    verificado: int = 0
    anulado: int = 0
    fecha_emision: str = ""
    personalizado_1: str = ""
    personalizado_2: str = ""
    personalizado_3: str = ""
    personalizado_4: str = ""
    personalizado_5: str = ""
    personalizado_6: str = ""
    personalizado_7: str = ""
    personalizado_8: str = ""
    personalizado_9: str = ""
    personalizado_10: str = ""
    personalizado_11: str = ""
    personalizado_12: str = ""
    personalizado_13: str = ""
    personalizado_14: str = ""
    personalizado_15: str = ""
    importacion: str = ""
    sucursal: str = ""
    clasificacion: str = ""


class OrdenCompra(BaseModel):
    """Schema para una orden de compra completa."""
    encabezado: OrdenCompraEncabezado
    detalles: List[OrdenCompraDetalle]


class SugeridoBulkExportResponse(BaseModel):
    """Schema de respuesta para actualización masiva a Exported."""
    message: str
    updated_count: int
    updated_ids: List[str]
    ordenes_compra: List[OrdenCompra] = []


class SugeridoReporteResponse(BaseModel):
    """Schema de respuesta para el reporte de sugerido de compras."""
    empresa: Optional[str] = Field(None, alias="empresa", title="Empresa")
    proveedor: Optional[str] = Field(None, alias="proveedor", title="Proveedor")
    cod_prod: Optional[str] = Field(None, alias="cod_prod", title="Codigo")
    descripcion: Optional[str] = Field(None, alias="descripcion", title="Descripción")
    unidad_medida: Optional[str] = Field(None, alias="unidad_medida", title="U Medida")
    cantidad_proveedor: Optional[Decimal] = Field(None, alias="cantidad_proveedor", title="Cantidad")
    valor_unitario_proveedor: Optional[Decimal] = Field(None, alias="valor_unitario_proveedor", title="Valor")
    tipo_doc_exp: Optional[str] = Field(None, alias="tipo_doc_exp", title="Tipo Doc Exp")
    prefijo_exp: Optional[str] = Field(None, alias="prefijo_exp", title="Prefijo Exp")
    num_doc_exp: Optional[str] = Field(None, alias="num_doc_exp", title="Numero Doc Exp")
    updated_at: Optional[datetime] = Field(None, alias="updated_at", title="Fecha Act")

    class Config:
        from_attributes = True


class SugeridoReporteListResponse(BaseModel):
    """Schema para lista del reporte."""
    items: List[SugeridoReporteResponse]
    total: int
