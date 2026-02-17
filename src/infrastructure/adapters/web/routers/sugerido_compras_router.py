"""
Router para Sugerido de Compras (Adaptador Web).
"""
from typing import Optional
from uuid import UUID
from datetime import date
from fastapi import APIRouter, Depends, Query

from domain.schemas.sugerido_compras_schema import (
    SugeridoComprasCreate,
    SugeridoComprasUpdate,
    SugeridoComprasResponse,
    SugeridoComprasListResponse,
    SugeridoComprasStatusUpdate,
    StatusSugerido,
    GenerarSugeridoRequest,
    SugeridoBulkUpdateRequest,
    SugeridoBulkUpdateResponse,
    SugeridoProcessedListResponse,
    SugeridoBulkExportRequest,
    SugeridoBulkExportResponse,
    SugeridoReporteListResponse
)
from application.use_cases.sugerido_compras_use_case import SugeridoComprasUseCase
from infrastructure.adapters.web.dependencies import get_sugerido_compras_use_case

router = APIRouter(prefix="/sugerido-compras", tags=["Sugerido de Compras"])


@router.post("/", response_model=SugeridoComprasResponse)
async def create_sugerido(
    data: SugeridoComprasCreate,
    use_case: SugeridoComprasUseCase = Depends(get_sugerido_compras_use_case)
):
    """Crear un nuevo registro de sugerido de compras."""
    return await use_case.create(data)


@router.get("/", response_model=SugeridoComprasListResponse)
async def get_all_sugeridos(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros"),
    use_case: SugeridoComprasUseCase = Depends(get_sugerido_compras_use_case)
):
    """Obtener todos los registros de sugerido de compras con paginación."""
    return await use_case.get_all(skip=skip, limit=limit)


@router.get("/by-status/{status}", response_model=SugeridoComprasListResponse)
async def get_sugeridos_by_status(
    status: StatusSugerido,
    use_case: SugeridoComprasUseCase = Depends(get_sugerido_compras_use_case)
):
    """Obtener registros por status."""
    return await use_case.get_by_status(status)


@router.get("/requested", response_model=SugeridoComprasListResponse)
async def get_sugeridos_requested(
    identificacion_tercero: Optional[str] = Query(None, description="Filtrar por identificación del tercero"),
    use_case: SugeridoComprasUseCase = Depends(get_sugerido_compras_use_case)
):
    """
    Obtener todos los registros con status 'Requested'.
    
    Si se proporciona el parámetro identificacion_tercero, filtra los resultados por ese valor.
    Si no se proporciona, retorna todos los registros con status 'Requested'.
    """
    return await use_case.get_requested_by_tercero(identificacion_tercero)


@router.get("/processed", response_model=SugeridoProcessedListResponse)
async def get_sugeridos_processed(
    use_case: SugeridoComprasUseCase = Depends(get_sugerido_compras_use_case)
):
    """
    Obtener todos los registros con status 'Processed'.
    
    Retorna solo los campos:
    - id
    - empresa
    - proveedor
    - cod_prod
    - descripcion
    - unidad_medida
    - cantidad_proveedor
    - valor_unitario_proveedor
    """
    return await use_case.get_processed()


@router.patch("/confirm")
async def confirm_sugerido_compras(
    use_case: SugeridoComprasUseCase = Depends(get_sugerido_compras_use_case)
):
    """
    Confirmar el sugerido de compras.
    
    Actualiza todos los registros con status 'Created' a 'Requested'.
    Retorna la cantidad de registros actualizados.
    """
    return await use_case.bulk_update_created_to_requested()


@router.post("/generar", response_model=SugeridoComprasListResponse)
async def generar_sugerido_compras(
    request: GenerarSugeridoRequest,
    use_case: SugeridoComprasUseCase = Depends(get_sugerido_compras_use_case)
):
    """
    Ejecutar el proceso de generación de sugerido de compras.
    
    Este endpoint:
    1. Ejecuta consultas complejas sobre Vista_Auxiliar_Movimientos_Inventario
    2. Calcula ventas, compras, entradas, salidas del periodo
    3. Obtiene los últimos 4 proveedores por producto
    4. Calcula el sugerido de compras basado en ventas del año anterior
    5. Excluye productos de la tabla inventario_excluido
    6. Inserta los resultados en sugerido_compras con status = 'Created'
    7. Retorna los registros creados
    
    **Filtros disponibles:**
    - fecha_inicial: Fecha inicio del periodo (requerido)
    - fecha_final: Fecha fin del periodo (requerido)
    - grupo3: Filtrar por Grupo 3 (opcional)
    - grupo4: Filtrar por Grupo 4 (opcional)
    - grupo5: Filtrar por Grupo 5 (opcional)
    """
    return await use_case.generar_sugerido(request)


@router.patch("/bulk-update-proveedor", response_model=SugeridoBulkUpdateResponse)
async def bulk_update_sugeridos_proveedor(
    request: SugeridoBulkUpdateRequest,
    use_case: SugeridoComprasUseCase = Depends(get_sugerido_compras_use_case)
):
    """
    Actualizar múltiples registros de sugerido de compras con datos del proveedor.
    
    Este endpoint:
    1. Recibe una lista de items con id, cantidad_proveedor y valor_unitario_proveedor
    2. Valida que cantidad_proveedor y valor_unitario_proveedor sean mayores a 0
    3. Actualiza los campos en la tabla sugerido_compras
    4. Cambia el status de cada registro a 'Processed'
    
    **Validaciones:**
    - cantidad_proveedor: Debe ser mayor a 0
    - valor_unitario_proveedor: Debe ser mayor a 0
    - Se requiere al menos un item en la lista
    """
    items_dict = [item.model_dump() for item in request.items]
    return await use_case.bulk_update_proveedor(items_dict)


@router.patch("/bulk-export", response_model=SugeridoBulkExportResponse)
async def bulk_export_sugeridos(
    request: SugeridoBulkExportRequest,
    use_case: SugeridoComprasUseCase = Depends(get_sugerido_compras_use_case)
):
    """
    Actualizar múltiples registros a status 'Exported'.
    
    Este endpoint:
    1. Recibe una lista de IDs de registros de sugerido_compras
    2. Actualiza el status de cada registro a 'Exported'
    3. Retorna la lista de IDs actualizados
    
    **Validaciones:**
    - Se requiere al menos un ID en la lista
    """
    return await use_case.bulk_update_to_exported(request.ids)


@router.get("/reporte", response_model=SugeridoReporteListResponse)
async def get_reporte_sugeridos(
    fecha_inicial: date = Query(..., description="Fecha inicial del periodo (YYYY-MM-DD)"),
    fecha_final: date = Query(..., description="Fecha final del periodo (YYYY-MM-DD)"),
    identificacion_tercero: Optional[str] = Query(None, description="NIT del proveedor"),
    status: Optional[str] = Query(None, description="Estado del registro (Created, Requested, Processed, Exported)"),
    use_case: SugeridoComprasUseCase = Depends(get_sugerido_compras_use_case)
):
    """
    Obtener reporte de sugerido de compras.
    
    **Filtros obligatorios:**
    - fecha_inicial: Fecha inicio del periodo (sobre updated_at)
    - fecha_final: Fecha fin del periodo (sobre updated_at)
    
    **Filtros opcionales:**
    - identificacion_tercero: NIT del proveedor
    - status: Estado del registro (Created, Requested, Processed, Exported)
    
    **Campos de respuesta:**
    Empresa, Proveedor, Codigo, Descripción, U Medida, Cantidad, Valor,
    Tipo Doc Exp, Prefijo Exp, Numero Doc Exp, Fecha Act
    
    Ordenado por Fecha Act descendente.
    """
    return await use_case.get_reporte(
        fecha_inicial=fecha_inicial,
        fecha_final=fecha_final,
        identificacion_tercero=identificacion_tercero,
        status_filter=status
    )


@router.patch("/{id}/reject", response_model=SugeridoComprasResponse)
async def reject_sugerido(
    id: UUID,
    use_case: SugeridoComprasUseCase = Depends(get_sugerido_compras_use_case)
):
    """
    Rechazar un registro de sugerido de compras.
    
    Cambia el status del registro a 'Rejected'.
    
    **Validaciones:**
    - El registro debe existir
    - El registro debe tener status 'Processed'
    """
    return await use_case.reject(id)


# Rutas con parámetro {id} al final para evitar conflictos de enrutamiento
@router.get("/{id}", response_model=SugeridoComprasResponse)
async def get_sugerido_by_id(
    id: UUID,
    use_case: SugeridoComprasUseCase = Depends(get_sugerido_compras_use_case)
):
    """Obtener un registro por ID."""
    return await use_case.get_by_id(id)


@router.put("/{id}", response_model=SugeridoComprasResponse)
async def update_sugerido(
    id: UUID,
    data: SugeridoComprasUpdate,
    use_case: SugeridoComprasUseCase = Depends(get_sugerido_compras_use_case)
):
    """Actualizar un registro."""
    return await use_case.update(id, data)


@router.patch("/{id}/status", response_model=SugeridoComprasResponse)
async def update_sugerido_status(
    id: UUID,
    data: SugeridoComprasStatusUpdate,
    use_case: SugeridoComprasUseCase = Depends(get_sugerido_compras_use_case)
):
    """Actualizar solo el status de un registro por ID."""
    return await use_case.update_status(id, data.status)


@router.delete("/{id}")
async def delete_sugerido(
    id: UUID,
    use_case: SugeridoComprasUseCase = Depends(get_sugerido_compras_use_case)
):
    """Eliminar un registro."""
    return await use_case.delete(id)


@router.delete("/by-status/{status}")
async def delete_sugeridos_by_status(
    status: StatusSugerido,
    use_case: SugeridoComprasUseCase = Depends(get_sugerido_compras_use_case)
):
    """Eliminar todos los registros con un status específico."""
    return await use_case.delete_by_status(status)

