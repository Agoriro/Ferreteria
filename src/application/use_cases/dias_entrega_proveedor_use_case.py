"""
Casos de uso de Días de Entrega por Proveedor - Lógica de negocio.
Principio SOLID: Open/Closed - Abierto a extensión, cerrado a modificación.
"""
from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from domain.ports.dias_entrega_proveedor_repository import DiasEntregaProveedorRepositoryPort
from domain.schemas.dias_entrega_proveedor_schema import (
    DiasEntregaProveedorCreate, 
    DiasEntregaProveedorUpdate,
    DiasEntregaProveedorListResponse,
    DiasEntregaProveedorResponse
)


class DiasEntregaProveedorUseCase:
    """
    Casos de uso para gestión de días de entrega por proveedor.
    Principio SOLID: Dependency Inversion - Depende de puerto, no de implementación.
    """
    
    def __init__(self, repository: DiasEntregaProveedorRepositoryPort):
        self.repository = repository
    
    async def create(self, data: DiasEntregaProveedorCreate):
        """Crea un nuevo registro de días de entrega."""
        # Verificar si ya existe un registro con la misma empresa y NIT
        existing = await self.repository.get_by_empresa_nit(data.empresa, data.nit_proveedor)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un registro con empresa '{data.empresa}' y NIT proveedor '{data.nit_proveedor}'"
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
        empresa: Optional[str] = None
    ) -> DiasEntregaProveedorListResponse:
        """Lista todos los registros con paginación, opcionalmente filtrados por empresa."""
        if empresa:
            items, total = await self.repository.get_by_empresa(empresa, skip, limit)
        else:
            items, total = await self.repository.get_all(skip, limit)
        
        return DiasEntregaProveedorListResponse(
            items=[DiasEntregaProveedorResponse.model_validate(item) for item in items],
            total=total,
            skip=skip,
            limit=limit
        )
    
    async def update(self, record_id: UUID, data: DiasEntregaProveedorUpdate):
        """Actualiza un registro."""
        # Verificar que el registro existe
        existing = await self.repository.get_by_id(record_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro no encontrado"
            )
        
        # Si se está actualizando empresa o NIT, verificar que no exista duplicado
        new_empresa = data.empresa if data.empresa else existing.empresa
        new_nit = data.nit_proveedor if data.nit_proveedor else existing.nit_proveedor
        
        if (data.empresa and data.empresa != existing.empresa) or \
           (data.nit_proveedor and data.nit_proveedor != existing.nit_proveedor):
            duplicate = await self.repository.get_by_empresa_nit(new_empresa, new_nit)
            if duplicate and duplicate.id != record_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe un registro con empresa '{new_empresa}' y NIT proveedor '{new_nit}'"
                )
        
        return await self.repository.update(record_id, data)
    
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



