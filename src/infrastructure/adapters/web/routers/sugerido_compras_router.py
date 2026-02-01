"""
Router para Sugerido de Compras (Adaptador Web).
"""
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query

from domain.schemas.sugerido_compras_schema import (
    SugeridoComprasCreate,
    SugeridoComprasUpdate,
    SugeridoComprasResponse,
    SugeridoComprasListResponse,
    SugeridoComprasStatusUpdate,
    StatusSugerido,
    GenerarSugeridoRequest
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

