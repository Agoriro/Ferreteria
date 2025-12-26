"""
Casos de uso de Inventario Excluido - Lógica de negocio.
Principio SOLID: Open/Closed - Abierto a extensión, cerrado a modificación.
"""
from typing import List
from uuid import UUID
from fastapi import HTTPException, status
from domain.ports.inventario_excluido_repository import InventarioExcluidoRepositoryPort
from domain.schemas.inventario_excluido_schema import (
    InventarioExcluidoCreate, 
    InventarioExcluidoUpdate,
    InventarioExcluidoListResponse,
    InventarioExcluidoResponse
)


class InventarioExcluidoUseCase:
    """
    Casos de uso para gestión de inventario excluido.
    Principio SOLID: Dependency Inversion - Depende de puerto, no de implementación.
    """
    
    def __init__(self, repository: InventarioExcluidoRepositoryPort):
        self.repository = repository
    
    async def create(self, data: InventarioExcluidoCreate):
        """Crea un nuevo registro de inventario excluido."""
        # Verificar si ya existe un registro con la misma empresa y código de producto
        existing = await self.repository.get_by_empresa_codigo(data.empresa, data.codigo_producto)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un registro con empresa '{data.empresa}' y código de producto '{data.codigo_producto}'"
            )
        
        return await self.repository.create(data)
    
    async def get_by_id(self, record_id: UUID):
        """Obtiene registro por ID."""
        record = await self.repository.get_by_id(record_id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro no encontrado"
            )
        return record
    
    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        include_inactive: bool = False
    ) -> InventarioExcluidoListResponse:
        """Lista todos los registros con paginación."""
        items, total = await self.repository.get_all(skip, limit, include_inactive)
        
        return InventarioExcluidoListResponse(
            items=[InventarioExcluidoResponse.model_validate(item) for item in items],
            total=total,
            skip=skip,
            limit=limit
        )
    
    async def update(self, record_id: UUID, data: InventarioExcluidoUpdate):
        """Actualiza un registro."""
        # Verificar que el registro existe
        existing = await self.repository.get_by_id(record_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro no encontrado"
            )
        
        # Si se está actualizando empresa o código de producto, verificar que no exista duplicado
        new_empresa = data.empresa if data.empresa else existing.empresa
        new_codigo = data.codigo_producto if data.codigo_producto else existing.codigo_producto
        
        if (data.empresa and data.empresa != existing.empresa) or \
           (data.codigo_producto and data.codigo_producto != existing.codigo_producto):
            duplicate = await self.repository.get_by_empresa_codigo(new_empresa, new_codigo)
            if duplicate and duplicate.id != record_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe un registro con empresa '{new_empresa}' y código de producto '{new_codigo}'"
                )
        
        return await self.repository.update(record_id, data)
    
    async def toggle_status(self, record_id: UUID, new_status: bool):
        """Cambia el estado de un registro (activo/inactivo)."""
        # Verificar que el registro existe
        existing = await self.repository.get_by_id(record_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro no encontrado"
            )
        
        success = await self.repository.toggle_status(record_id, new_status)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar el estado"
            )
        
        # Retornar el registro actualizado
        return await self.repository.get_by_id(record_id)
    
    async def delete(self, record_id: UUID):
        """Elimina un registro permanentemente."""
        # Verificar que el registro existe
        existing = await self.repository.get_by_id(record_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro no encontrado"
            )
        
        success = await self.repository.delete(record_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar el registro"
            )
        
        return {"message": "Registro eliminado exitosamente"}

