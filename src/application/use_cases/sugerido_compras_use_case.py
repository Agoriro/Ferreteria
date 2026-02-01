"""
Casos de uso para Sugerido de Compras.
"""
from typing import List, Optional
from uuid import UUID
from datetime import date
from fastapi import HTTPException, status

from domain.ports.sugerido_compras_repository import SugeridoComprasRepositoryPort
from domain.schemas.sugerido_compras_schema import (
    SugeridoComprasCreate,
    SugeridoComprasUpdate,
    SugeridoComprasResponse,
    SugeridoComprasListResponse,
    StatusSugerido,
    GenerarSugeridoRequest
)


class SugeridoComprasUseCase:
    """Casos de uso para Sugerido de Compras."""
    
    def __init__(self, repository: SugeridoComprasRepositoryPort):
        self.repository = repository
    
    async def create(self, data: SugeridoComprasCreate) -> SugeridoComprasResponse:
        """Crear un nuevo registro de sugerido de compras."""
        return await self.repository.create(data)
    
    async def get_by_id(self, id: UUID) -> SugeridoComprasResponse:
        """Obtener un registro por ID."""
        result = await self.repository.get_by_id(id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Registro con ID {id} no encontrado"
            )
        return result
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> SugeridoComprasListResponse:
        """Obtener todos los registros con paginación."""
        items = await self.repository.get_all(skip=skip, limit=limit)
        return SugeridoComprasListResponse(items=items, total=len(items))
    
    async def get_by_status(self, status_filter: StatusSugerido) -> SugeridoComprasListResponse:
        """Obtener registros por status."""
        items = await self.repository.get_by_status(status_filter)
        return SugeridoComprasListResponse(items=items, total=len(items))
    
    async def update(self, id: UUID, data: SugeridoComprasUpdate) -> SugeridoComprasResponse:
        """Actualizar un registro."""
        result = await self.repository.update(id, data)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Registro con ID {id} no encontrado"
            )
        return result
    
    async def update_status(self, id: UUID, new_status: StatusSugerido) -> SugeridoComprasResponse:
        """Actualizar solo el status de un registro."""
        result = await self.repository.update_status(id, new_status)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Registro con ID {id} no encontrado"
            )
        return result
    
    async def delete(self, id: UUID) -> dict:
        """Eliminar un registro."""
        success = await self.repository.delete(id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Registro con ID {id} no encontrado"
            )
        return {"message": "Registro eliminado correctamente", "id": str(id)}
    
    async def delete_by_status(self, status_filter: StatusSugerido) -> dict:
        """Eliminar registros por status."""
        count = await self.repository.delete_by_status(status_filter)
        return {
            "message": f"Registros con status '{status_filter.value}' eliminados",
            "count": count
        }
    
    async def generar_sugerido(self, request: GenerarSugeridoRequest) -> SugeridoComprasListResponse:
        """
        Ejecutar el proceso de generación de sugerido de compras.
        
        1. Ejecuta las consultas complejas sobre Vista_Auxiliar_Movimientos_Inventario
        2. Excluye productos de inventario_excluido
        3. Inserta los resultados en sugerido_compras con status = 'Created'
        4. Retorna los registros creados
        """
        # Validar fechas
        if request.fecha_final < request.fecha_inicial:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha final debe ser mayor o igual a la fecha inicial"
            )
        
        # Ejecutar el proceso
        items = await self.repository.generar_sugerido(
            fecha_inicial=request.fecha_inicial,
            fecha_final=request.fecha_final,
            grupo3=request.grupo3,
            grupo4=request.grupo4,
            grupo5=request.grupo5
        )
        
        return SugeridoComprasListResponse(items=items, total=len(items))

