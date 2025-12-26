"""
Implementación concreta del repositorio de Vista_Tabla_Inventarios (Adaptador).
Principio SOLID: Liskov Substitution - Puede reemplazar la abstracción.
"""
from typing import List, Optional, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from domain.ports.vista_inventarios_repository import VistaInventariosRepositoryPort
from infrastructure.models.sqlalchemy_models import VistaTablaInventariosModel


class SQLAlchemyVistaInventariosRepository(VistaInventariosRepositoryPort):
    """Adaptador de persistencia para Vista_Tabla_Inventarios usando SQLAlchemy."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_all_basic(
        self, 
        skip: int = 0, 
        limit: int = 100,
        empresa: str = None
    ) -> Tuple[List, int]:
        """
        Lista todos los inventarios con campos básicos.
        Solo retorna: empresa, codigo_producto, descripcion.
        """
        # Query base - solo seleccionamos los campos necesarios
        base_query = select(
            VistaTablaInventariosModel.empresa,
            VistaTablaInventariosModel.codigo_producto,
            VistaTablaInventariosModel.descripcion
        )
        count_query = select(func.count()).select_from(VistaTablaInventariosModel)
        
        # Filtro por empresa si se proporciona
        if empresa:
            base_query = base_query.where(VistaTablaInventariosModel.empresa == empresa)
            count_query = count_query.where(VistaTablaInventariosModel.empresa == empresa)
        
        # Obtener total
        total_result = await self.session.execute(count_query)
        total = total_result.scalar()
        
        # Obtener registros paginados ordenados por código de producto
        stmt = base_query.offset(skip).limit(limit).order_by(VistaTablaInventariosModel.codigo_producto)
        result = await self.session.execute(stmt)
        items = result.all()
        
        return items, total

