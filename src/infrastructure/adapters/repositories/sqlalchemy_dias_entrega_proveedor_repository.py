"""
Implementación concreta del repositorio de días de entrega por proveedor (Adaptador).
Principio SOLID: Liskov Substitution - Puede reemplazar la abstracción.
"""
from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy import select, update, delete, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from domain.ports.dias_entrega_proveedor_repository import DiasEntregaProveedorRepositoryPort
from domain.schemas.dias_entrega_proveedor_schema import (
    DiasEntregaProveedorCreate, 
    DiasEntregaProveedorUpdate,
    ProductoOption,
    ProveedorOption
)
from infrastructure.models.sqlalchemy_models import DiasEntregaProveedorModel


class SQLAlchemyDiasEntregaProveedorRepository(DiasEntregaProveedorRepositoryPort):
    """Adaptador de persistencia para días de entrega por proveedor usando SQLAlchemy."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, data: DiasEntregaProveedorCreate) -> DiasEntregaProveedorModel:
        """Crea un nuevo registro de días de entrega."""
        db_record = DiasEntregaProveedorModel(
            empresa=data.empresa,
            nit_proveedor=data.nit_proveedor,
            codigo_producto=data.codigo_producto,
            dias_entrega=data.dias_entrega
        )
        
        self.session.add(db_record)
        await self.session.commit()
        await self.session.refresh(db_record)
        return db_record
    
    async def get_by_id(self, record_id: UUID) -> Optional[DiasEntregaProveedorModel]:
        """Obtiene registro por ID."""
        stmt = select(DiasEntregaProveedorModel).where(DiasEntregaProveedorModel.id == record_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_empresa_nit_producto(
        self, 
        empresa: str, 
        nit_proveedor: str, 
        codigo_producto: str
    ) -> Optional[DiasEntregaProveedorModel]:
        """Obtiene registro por empresa, NIT del proveedor y código de producto (combinación única)."""
        stmt = select(DiasEntregaProveedorModel).where(
            DiasEntregaProveedorModel.empresa == empresa,
            DiasEntregaProveedorModel.nit_proveedor == nit_proveedor,
            DiasEntregaProveedorModel.codigo_producto == codigo_producto
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> Tuple[List[DiasEntregaProveedorModel], int]:
        """Lista todos los registros con paginación."""
        # Query base
        base_query = select(DiasEntregaProveedorModel)
        count_query = select(func.count()).select_from(DiasEntregaProveedorModel)
        
        # Obtener total
        total_result = await self.session.execute(count_query)
        total = total_result.scalar()
        
        # Obtener registros paginados
        stmt = base_query.offset(skip).limit(limit).order_by(
            DiasEntregaProveedorModel.empresa, 
            DiasEntregaProveedorModel.codigo_producto,
            DiasEntregaProveedorModel.nit_proveedor
        )
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        
        return items, total
    
    async def get_by_empresa(
        self, 
        empresa: str,
        skip: int = 0, 
        limit: int = 100
    ) -> Tuple[List[DiasEntregaProveedorModel], int]:
        """Lista registros filtrados por empresa."""
        # Query base con filtro
        base_query = select(DiasEntregaProveedorModel).where(
            DiasEntregaProveedorModel.empresa == empresa
        )
        count_query = select(func.count()).select_from(DiasEntregaProveedorModel).where(
            DiasEntregaProveedorModel.empresa == empresa
        )
        
        # Obtener total
        total_result = await self.session.execute(count_query)
        total = total_result.scalar()
        
        # Obtener registros paginados
        stmt = base_query.offset(skip).limit(limit).order_by(
            DiasEntregaProveedorModel.codigo_producto,
            DiasEntregaProveedorModel.nit_proveedor
        )
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        
        return items, total
    
    async def get_by_producto(
        self, 
        empresa: str,
        codigo_producto: str,
        skip: int = 0, 
        limit: int = 100
    ) -> Tuple[List[DiasEntregaProveedorModel], int]:
        """Lista registros filtrados por empresa y producto."""
        base_query = select(DiasEntregaProveedorModel).where(
            DiasEntregaProveedorModel.empresa == empresa,
            DiasEntregaProveedorModel.codigo_producto == codigo_producto
        )
        count_query = select(func.count()).select_from(DiasEntregaProveedorModel).where(
            DiasEntregaProveedorModel.empresa == empresa,
            DiasEntregaProveedorModel.codigo_producto == codigo_producto
        )
        
        total_result = await self.session.execute(count_query)
        total = total_result.scalar()
        
        stmt = base_query.offset(skip).limit(limit).order_by(DiasEntregaProveedorModel.dias_entrega)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        
        return items, total
    
    async def update(self, record_id: UUID, data: DiasEntregaProveedorUpdate) -> Optional[DiasEntregaProveedorModel]:
        """Actualiza un registro."""
        update_data = data.model_dump(exclude_unset=True)
        
        if update_data:
            stmt = (
                update(DiasEntregaProveedorModel)
                .where(DiasEntregaProveedorModel.id == record_id)
                .values(**update_data)
                .returning(DiasEntregaProveedorModel)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one_or_none()
        
        return await self.get_by_id(record_id)
    
    async def delete(self, record_id: UUID) -> bool:
        """Elimina un registro permanentemente."""
        stmt = delete(DiasEntregaProveedorModel).where(DiasEntregaProveedorModel.id == record_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def get_productos_by_empresa(
        self, 
        empresa: str,
        search: Optional[str] = None,
        limit: int = 50
    ) -> List[ProductoOption]:
        """
        Obtiene lista de productos para dropdown filtrados por empresa.
        Busca en Vista_Tabla_Inventarios.
        """
        search_filter = ""
        if search:
            search_filter = f"""
                AND (
                    LOWER(inv."Codigo_Producto") LIKE LOWER('%{search}%')
                    OR LOWER(inv."Descripcion") LIKE LOWER('%{search}%')
                )
            """
        
        query = text(f"""
            SELECT DISTINCT
                inv."Codigo_Producto" as codigo_producto,
                inv."Descripcion" as descripcion
            FROM "public"."Vista_Tabla_Inventarios" inv
            WHERE inv."Empresa" = :empresa
              AND inv."Clasificacion" = 'Producto'
              {search_filter}
            ORDER BY inv."Codigo_Producto"
            LIMIT :limit
        """)
        
        result = await self.session.execute(query, {"empresa": empresa, "limit": limit})
        rows = result.fetchall()
        
        return [
            ProductoOption(
                codigo_producto=row.codigo_producto,
                descripcion=row.descripcion or ""
            )
            for row in rows
        ]
    
    async def get_proveedores_by_empresa(
        self, 
        empresa: str,
        search: Optional[str] = None,
        limit: int = 50
    ) -> List[ProveedorOption]:
        """
        Obtiene lista de proveedores para dropdown filtrados por empresa.
        Busca proveedores únicos en Vista_Auxiliar_Movimientos_Inventario.
        """
        search_filter = ""
        if search:
            search_filter = f"""
                AND (
                    LOWER(mov."Identificacion_Tercero") LIKE LOWER('%{search}%')
                    OR LOWER(mov."Tercero") LIKE LOWER('%{search}%')
                )
            """
        
        query = text(f"""
            SELECT DISTINCT
                mov."Identificacion_Tercero" as nit_proveedor,
                mov."Tercero" as nombre_proveedor
            FROM "public"."Vista_Auxiliar_Movimientos_Inventario" mov
            WHERE mov."Empresa" = :empresa
              AND mov."Tipo_Documento" = 'FC'
              AND mov."Identificacion_Tercero" IS NOT NULL
              AND mov."Identificacion_Tercero" != ''
              {search_filter}
            ORDER BY mov."Tercero"
            LIMIT :limit
        """)
        
        result = await self.session.execute(query, {"empresa": empresa, "limit": limit})
        rows = result.fetchall()
        
        return [
            ProveedorOption(
                nit_proveedor=row.nit_proveedor,
                nombre_proveedor=row.nombre_proveedor or ""
            )
            for row in rows
        ]
    
    async def get_min_dias_entrega(
        self, 
        empresa: str, 
        codigo_producto: str
    ) -> Optional[int]:
        """
        Obtiene el mínimo de días de entrega para un producto en una empresa.
        Útil para el cálculo del sugerido de compras.
        """
        query = text("""
            SELECT MIN(dias_entrega) as min_dias
            FROM "public".dias_entrega_proveedor
            WHERE empresa = :empresa
              AND codigo_producto = :codigo_producto
        """)
        
        result = await self.session.execute(
            query, 
            {"empresa": empresa, "codigo_producto": codigo_producto}
        )
        row = result.fetchone()
        
        return row.min_dias if row and row.min_dias is not None else None
