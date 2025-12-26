"""
Casos de uso de Vista_Tabla_Inventarios - Lógica de negocio.
Principio SOLID: Open/Closed - Abierto a extensión, cerrado a modificación.
"""
from typing import Optional
from domain.ports.vista_inventarios_repository import VistaInventariosRepositoryPort
from domain.schemas.vista_inventarios_schema import (
    VistaInventariosListResponse,
    VistaInventarioItem
)


class VistaInventariosUseCase:
    """
    Casos de uso para consulta de inventarios.
    Principio SOLID: Dependency Inversion - Depende de puerto, no de implementación.
    """
    
    def __init__(self, repository: VistaInventariosRepositoryPort):
        self.repository = repository
    
    async def get_all_basic(
        self, 
        skip: int = 0, 
        limit: int = 100,
        empresa: Optional[str] = None
    ) -> VistaInventariosListResponse:
        """
        Lista todos los inventarios con campos básicos (empresa, codigo_producto, descripcion).
        
        Args:
            skip: Número de registros a saltar para paginación
            limit: Número máximo de registros a retornar
            empresa: Filtro opcional por empresa
        """
        items, total = await self.repository.get_all_basic(skip, limit, empresa)
        
        # Convertir las tuplas a objetos VistaInventarioItem
        return VistaInventariosListResponse(
            items=[
                VistaInventarioItem(
                    empresa=item.empresa,
                    codigo_producto=item.codigo_producto,
                    descripcion=item.descripcion
                ) 
                for item in items
            ],
            total=total,
            skip=skip,
            limit=limit
        )

