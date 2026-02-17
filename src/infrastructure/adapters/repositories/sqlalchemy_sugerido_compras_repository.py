"""
Implementación SQLAlchemy del repositorio de Sugerido de Compras.
"""
import logging
import math
from typing import List, Optional
from uuid import UUID
from datetime import date
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, text, and_, bindparam
from sqlalchemy.orm import selectinload

logger = logging.getLogger(__name__)

from domain.ports.sugerido_compras_repository import SugeridoComprasRepositoryPort
from domain.schemas.sugerido_compras_schema import (
    SugeridoComprasCreate,
    SugeridoComprasUpdate,
    SugeridoComprasResponse,
    StatusSugerido
)
from infrastructure.models.sqlalchemy_models import SugeridoComprasModel, StatusSugerido as ModelStatusSugerido, VistaTablaInventariosModel


class SQLAlchemySugeridoComprasRepository(SugeridoComprasRepositoryPort):
    """Implementación concreta del repositorio usando SQLAlchemy."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def _model_to_response(self, model: SugeridoComprasModel) -> SugeridoComprasResponse:
        """Convierte modelo a schema de respuesta."""
        return SugeridoComprasResponse(
            id=model.id,
            empresa=model.empresa,
            fecha=model.fecha,
            num_doc=model.num_doc,
            proveedor=model.proveedor,
            grupo3=model.grupo3,
            grupo4=model.grupo4,
            grupo5=model.grupo5,
            cod_prod=model.cod_prod,
            descripcion=model.descripcion,
            unidad_medida=model.unidad_medida,
            exist=model.exist,
            exist_mc=model.exist_mc,
            cantidad_ventas_anterior=model.cantidad_ventas_anterior,
            cantidad_ventas_actual=model.cantidad_ventas_actual,
            sugerido_compras=model.sugerido_compras,
            cantidad_a_pedir=model.cantidad_a_pedir,
            proveedor1=model.proveedor1,
            proveedor2=model.proveedor2,
            proveedor3=model.proveedor3,
            proveedor4=model.proveedor4,
            compras_en_el_periodo=model.compras_en_el_periodo,
            total_entradas_en_el_periodo=model.total_entradas_en_el_periodo,
            ultima_fecha_compra=model.ultima_fecha_compra,
            ventas_en_el_periodo=model.ventas_en_el_periodo,
            total_salidas_en_el_periodo=model.total_salidas_en_el_periodo,
            ultima_fecha_venta=model.ultima_fecha_venta,
            saldo_actual=model.saldo_actual,
            val_unit=model.val_unit,
            dcto=model.dcto,
            val_neto=model.val_neto,
            precio1=model.precio1,
            util_1=model.util_1,
            precio2=model.precio2,
            util_2=model.util_2,
            cantidad_proveedor=model.cantidad_proveedor,
            valor_unitario_proveedor=model.valor_unitario_proveedor,
            status=StatusSugerido(model.status.value),
            created_at=model.created_at
        )
    
    async def create(self, data: SugeridoComprasCreate) -> SugeridoComprasResponse:
        """Crear un nuevo registro."""
        model = SugeridoComprasModel(
            **data.model_dump(exclude={"status"}),
            status=ModelStatusSugerido(data.status.value)
        )
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return self._model_to_response(model)
    
    async def get_by_id(self, id: UUID) -> Optional[SugeridoComprasResponse]:
        """Obtener un registro por ID."""
        result = await self.db.execute(
            select(SugeridoComprasModel).where(SugeridoComprasModel.id == id)
        )
        model = result.scalar_one_or_none()
        return self._model_to_response(model) if model else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[SugeridoComprasResponse]:
        """Obtener todos los registros con paginación."""
        result = await self.db.execute(
            select(SugeridoComprasModel)
            .order_by(SugeridoComprasModel.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._model_to_response(m) for m in models]
    
    async def get_by_status(self, status: StatusSugerido) -> List[SugeridoComprasResponse]:
        """Obtener registros por status."""
        result = await self.db.execute(
            select(SugeridoComprasModel)
            .where(SugeridoComprasModel.status == ModelStatusSugerido(status.value))
            .order_by(SugeridoComprasModel.proveedor.desc())
        )
        models = result.scalars().all()
        return [self._model_to_response(m) for m in models]
    
    async def update(self, id: UUID, data: SugeridoComprasUpdate) -> Optional[SugeridoComprasResponse]:
        """Actualizar un registro."""
        result = await self.db.execute(
            select(SugeridoComprasModel).where(SugeridoComprasModel.id == id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        if 'status' in update_data and update_data['status']:
            update_data['status'] = ModelStatusSugerido(update_data['status'].value)
        
        for field, value in update_data.items():
            setattr(model, field, value)
        
        await self.db.commit()
        await self.db.refresh(model)
        return self._model_to_response(model)
    
    async def update_status(self, id: UUID, status: StatusSugerido) -> Optional[SugeridoComprasResponse]:
        """Actualizar solo el status de un registro."""
        result = await self.db.execute(
            select(SugeridoComprasModel).where(SugeridoComprasModel.id == id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            return None
        
        model.status = ModelStatusSugerido(status.value)
        await self.db.commit()
        await self.db.refresh(model)
        return self._model_to_response(model)
    
    async def delete(self, id: UUID) -> bool:
        """Eliminar un registro."""
        result = await self.db.execute(
            delete(SugeridoComprasModel).where(SugeridoComprasModel.id == id)
        )
        await self.db.commit()
        return result.rowcount > 0
    
    async def delete_by_status(self, status: StatusSugerido) -> int:
        """Eliminar registros por status."""
        result = await self.db.execute(
            delete(SugeridoComprasModel)
            .where(SugeridoComprasModel.status == ModelStatusSugerido(status.value))
        )
        await self.db.commit()
        return result.rowcount
    
    async def bulk_update_created_to_requested(self) -> int:
        """Actualizar todos los registros con status 'Created' a 'Requested'."""
        result = await self.db.execute(
            update(SugeridoComprasModel)
            .where(SugeridoComprasModel.status == ModelStatusSugerido.Created)
            .values(status=ModelStatusSugerido.Requested)
        )
        await self.db.commit()
        return result.rowcount
    
    async def bulk_create(self, items: List[SugeridoComprasCreate]) -> int:
        """Crear múltiples registros."""
        models = [
            SugeridoComprasModel(
                **item.model_dump(exclude={"status"}),
                status=ModelStatusSugerido(item.status.value)
            )
            for item in items
        ]
        self.db.add_all(models)
        await self.db.commit()
        return len(models)
    
    async def get_requested_by_tercero(self, identificacion_tercero: Optional[str] = None) -> List[SugeridoComprasResponse]:
        """
        Obtener registros con status 'Requested'.
        Si se proporciona identificacion_tercero, filtra por ese valor.
        """
        query = select(SugeridoComprasModel).where(
            SugeridoComprasModel.status == ModelStatusSugerido.Requested
        )
        
        if identificacion_tercero:
            query = query.where(
                SugeridoComprasModel.identificacion_tercero == identificacion_tercero
            )
        
        query = query.order_by(SugeridoComprasModel.cod_prod)
        
        result = await self.db.execute(query)
        models = result.scalars().all()
        return [self._model_to_response(m) for m in models]
    
    async def bulk_update_proveedor(self, items: List[dict]) -> List[UUID]:
        """
        Actualizar cantidad_proveedor, valor_unitario_proveedor y cambiar status a 'Processed'.
        Retorna lista de IDs actualizados.
        """
        updated_ids = []
        
        for item in items:
            item_id = item['id']
            cantidad = item['cantidad_proveedor']
            valor = item['valor_unitario_proveedor']
            
            # Buscar el registro
            result = await self.db.execute(
                select(SugeridoComprasModel).where(SugeridoComprasModel.id == item_id)
            )
            model = result.scalar_one_or_none()
            
            if model:
                model.cantidad_proveedor = cantidad
                model.valor_unitario_proveedor = valor
                model.status = ModelStatusSugerido.Processed
                updated_ids.append(item_id)
        
        await self.db.commit()
        return updated_ids
    
    async def get_processed(self) -> List[dict]:
        """
        Obtener registros con status 'Processed' con campos reducidos.
        """
        result = await self.db.execute(
            select(
                SugeridoComprasModel.id,
                SugeridoComprasModel.empresa,
                SugeridoComprasModel.proveedor,
                SugeridoComprasModel.cod_prod,
                SugeridoComprasModel.descripcion,
                SugeridoComprasModel.unidad_medida,
                SugeridoComprasModel.cantidad_proveedor,
                SugeridoComprasModel.valor_unitario_proveedor
            )
            .where(SugeridoComprasModel.status == ModelStatusSugerido.Processed)
            .order_by(SugeridoComprasModel.cod_prod)
        )
        rows = result.fetchall()
        return [
            {
                "id": row.id,
                "empresa": row.empresa,
                "proveedor": row.proveedor,
                "cod_prod": row.cod_prod,
                "descripcion": row.descripcion,
                "unidad_medida": row.unidad_medida,
                "cantidad_proveedor": row.cantidad_proveedor,
                "valor_unitario_proveedor": row.valor_unitario_proveedor
            }
            for row in rows
        ]
    
    async def bulk_update_to_exported(self, ids: List[UUID], doc_info_map: dict = None) -> List[UUID]:
        """
        Actualizar múltiples registros a status 'Exported' y guardar datos del documento de exportación.
        
        Args:
            ids: Lista de IDs a actualizar.
            doc_info_map: Diccionario {id: {"tipo_doc": str, "prefijo": str, "num_doc": str}}
        """
        updated_ids = []
        
        for item_id in ids:
            result = await self.db.execute(
                select(SugeridoComprasModel).where(SugeridoComprasModel.id == item_id)
            )
            model = result.scalar_one_or_none()
            
            if model:
                model.status = ModelStatusSugerido.Exported
                if doc_info_map and item_id in doc_info_map:
                    info = doc_info_map[item_id]
                    model.tipo_doc_exp = info.get("tipo_doc", "")
                    model.prefijo_exp = info.get("prefijo", "")
                    model.num_doc_exp = info.get("num_doc", "")
                updated_ids.append(item_id)
        
        await self.db.commit()
        return updated_ids
    
    async def get_max_documento_oc(self) -> int:
        """
        Obtener el máximo Numero_Documento de Vista_Auxiliar_Movimientos_Inventario
        donde Tipo_Documento = 'OC' y prefijo = 'CO'.
        """
        query = text("""
            SELECT COALESCE(MAX(CAST("Numero_Documento" AS INTEGER)), 0) as max_doc
            FROM "public"."Vista_Auxiliar_Movimientos_Inventario"
            WHERE "Tipo_Documento" = 'OC' AND "prefijo" = 'CO'
        """)
        result = await self.db.execute(query)
        row = result.fetchone()
        return row.max_doc if row and row.max_doc else 0
    
    async def get_productos_iva(self, cod_prods: List[str]) -> dict:
        """
        Obtener IVA de Vista_Tabla_Inventarios por códigos de producto.
        """
        if not cod_prods:
            return {}
        
        result = await self.db.execute(
            select(
                VistaTablaInventariosModel.codigo_producto,
                VistaTablaInventariosModel.iva
            )
            .where(VistaTablaInventariosModel.codigo_producto.in_(cod_prods))
        )
        rows = result.fetchall()
        return {row.codigo_producto: round(float(row.iva or 0), 2) for row in rows}
    
    async def get_sugeridos_for_export(self, ids: List[UUID]) -> List[dict]:
        """
        Obtener registros completos de sugerido_compras por IDs.
        """
        if not ids:
            return []
        
        result = await self.db.execute(
            select(SugeridoComprasModel)
            .where(SugeridoComprasModel.id.in_(ids))
            .order_by(SugeridoComprasModel.empresa, SugeridoComprasModel.identificacion_tercero, SugeridoComprasModel.cod_prod)
        )
        models = result.scalars().all()
        return [
            {
                "id": model.id,
                "empresa": model.empresa,
                "proveedor": model.proveedor,
                "identificacion_tercero": model.identificacion_tercero,
                "cod_prod": model.cod_prod,
                "descripcion": model.descripcion,
                "unidad_medida": model.unidad_medida,
                "cantidad_proveedor": model.cantidad_proveedor,
                "valor_unitario_proveedor": model.valor_unitario_proveedor
            }
            for model in models
        ]
    
    async def generar_sugerido(
        self,
        fecha_inicial: date,
        fecha_final: date,
        grupo3: Optional[str] = None,
        grupo4: Optional[str] = None,
        grupo5: Optional[str] = None
    ) -> List[SugeridoComprasResponse]:
        """
        Ejecutar el proceso completo de generación de sugerido de compras.
        
        Fórmula:
        - Demanda_diaria = ventas_en_el_periodo / días_del_periodo
        - Tiempo_entrega = MIN(dias_entrega) de dias_entrega_proveedor (por empresa + proveedor)
        - Días_margen = Tiempo_entrega (mismo valor)
        - Stock_seguridad = Demanda_diaria × Días_margen
        - Sugerido = (Demanda_diaria × Tiempo_entrega) + Stock_seguridad
                   = 2 × Demanda_diaria × MIN(dias_entrega)
        """
        
        # Eliminar registros anteriores con status Created antes de generar nuevos
        deleted_count = await self.delete_by_status(StatusSugerido.Created)
        logger.info(f"Eliminados {deleted_count} registros con status 'Created' antes de generar sugerido")
        
        # Construir filtros opcionales usando parámetros bound (seguro contra SQL injection)
        filtro_grupo3 = "AND inv.\"Descripcion_Grupo_Tres\" = :grupo3" if grupo3 else ""
        filtro_grupo4 = "AND inv.\"Descripcion_Grupo_Cuatro\" = :grupo4" if grupo4 else ""
        filtro_grupo5 = "AND inv.\"Descripcion_Grupo_Cinco\" = :grupo5" if grupo5 else ""
        
        # Query completa usando CTEs
        query = text(f"""
        WITH 
        -- Calcular días del periodo
        dias_periodo AS (
            SELECT (CAST(:fecha_final AS DATE) - CAST(:fecha_inicial AS DATE) + 1) as dias
        ),
        
        -- Mínimo de días de entrega por empresa y proveedor
        min_dias_entrega AS (
            SELECT 
                dep.empresa,
                dep.nit_proveedor,
                MIN(dep.dias_entrega) as dias_entrega
            FROM "public".dias_entrega_proveedor dep
            GROUP BY dep.empresa, dep.nit_proveedor
        ),
        
        -- Proveedores por producto (últimos 4)
        proveedores AS (
            SELECT * FROM (
                SELECT 
                    mov."CodigoInventario",
                    mov."Empresa",
                    mov."Identificacion_Tercero" || ' - ' || mov."Tercero" as proveedor,
                    mov."Tercero" as proveedor_nombre,
                    mov."Identificacion_Tercero" as identificacion_tercero,
                    ROW_NUMBER() OVER (
                        PARTITION BY mov."CodigoInventario", mov."Empresa"
                        ORDER BY MAX(mov."Fecha") DESC
                    ) AS num_linea
                FROM "public"."Vista_Auxiliar_Movimientos_Inventario" mov
                WHERE mov."Tipo_Documento" = 'FC'
                GROUP BY mov."CodigoInventario", mov."Empresa", mov."Identificacion_Tercero", mov."Tercero"
            ) t
            WHERE num_linea <= 4
        ),
        
        -- Proveedores pivoteados
        prov_pivot AS (
            SELECT 
                "CodigoInventario",
                "Empresa",
                MAX(CASE WHEN num_linea = 1 THEN proveedor END) as prov1,
                MAX(CASE WHEN num_linea = 1 THEN proveedor_nombre END) as prov1_nombre,
                MAX(CASE WHEN num_linea = 1 THEN identificacion_tercero END) as prov1_identificacion,
                MAX(CASE WHEN num_linea = 2 THEN proveedor END) as prov2,
                MAX(CASE WHEN num_linea = 3 THEN proveedor END) as prov3,
                MAX(CASE WHEN num_linea = 4 THEN proveedor END) as prov4
            FROM proveedores
            GROUP BY "CodigoInventario", "Empresa"
        ),
        
        -- Ventas en el periodo
        ventas AS (
            SELECT 
                mov."CodigoInventario",
                mov."Empresa",
                SUM(ABS(COALESCE(CAST(mov."Cant" AS NUMERIC), 0))) as ventas,
                MAX(mov."Fecha") as max_fecha_fv
            FROM "public"."Vista_Auxiliar_Movimientos_Inventario" mov
            WHERE mov."Tipo_Documento" IN ('FV', 'DMC')
              AND mov."Fecha" BETWEEN :fecha_inicial AND :fecha_final
            GROUP BY mov."CodigoInventario", mov."Empresa"
        ),
        
        -- Ventas año anterior
        ventas_anio_anterior AS (
            SELECT 
                mov."CodigoInventario",
                mov."Empresa",
                SUM(ABS(COALESCE(CAST(mov."Cant" AS NUMERIC), 0))) as cantidad
            FROM "public"."Vista_Auxiliar_Movimientos_Inventario" mov
            WHERE mov."Tipo_Documento" IN ('FV', 'DMC')
              AND mov."Fecha" BETWEEN (CAST(:fecha_inicial AS DATE) - INTERVAL '1 year') AND (CAST(:fecha_final AS DATE) - INTERVAL '1 year')
            GROUP BY mov."CodigoInventario", mov."Empresa"
        ),
        
        -- Ventas año actual
        ventas_anio_actual AS (
            SELECT 
                mov."CodigoInventario",
                mov."Empresa",
                SUM(ABS(COALESCE(CAST(mov."Cant" AS NUMERIC), 0))) as cantidad
            FROM "public"."Vista_Auxiliar_Movimientos_Inventario" mov
            WHERE mov."Tipo_Documento" IN ('FV', 'DMC')
              AND mov."Fecha" BETWEEN :fecha_inicial AND :fecha_final
            GROUP BY mov."CodigoInventario", mov."Empresa"
        ),
        
        -- Compras en el periodo
        compras AS (
            SELECT 
                mov."CodigoInventario",
                mov."Empresa",
                SUM(ABS(COALESCE(CAST(mov."Cant" AS NUMERIC), 0))) as compras,
                MAX(mov."Fecha") as max_fecha_fc
            FROM "public"."Vista_Auxiliar_Movimientos_Inventario" mov
            WHERE mov."Tipo_Documento" IN ('FC', 'DMP')
              AND mov."Fecha" BETWEEN :fecha_inicial AND :fecha_final
            GROUP BY mov."CodigoInventario", mov."Empresa"
        ),
        
        -- Entradas en el periodo
        entradas AS (
            SELECT 
                mov."CodigoInventario",
                mov."Empresa",
                SUM(ABS(COALESCE(CAST(mov."Cant" AS NUMERIC), 0))) as entradas
            FROM "public"."Vista_Auxiliar_Movimientos_Inventario" mov
            WHERE mov."Tipo_Documento" IN ('EA', 'EPT')
              AND mov."Fecha" BETWEEN :fecha_inicial AND :fecha_final
            GROUP BY mov."CodigoInventario", mov."Empresa"
        ),
        
        -- Salidas en el periodo
        salidas AS (
            SELECT 
                mov."CodigoInventario",
                mov."Empresa",
                SUM(ABS(COALESCE(CAST(mov."Cant" AS NUMERIC), 0))) as salidas
            FROM "public"."Vista_Auxiliar_Movimientos_Inventario" mov
            WHERE mov."Tipo_Documento" = 'SA'
              AND mov."Fecha" BETWEEN :fecha_inicial AND :fecha_final
            GROUP BY mov."CodigoInventario", mov."Empresa"
        ),
        
        -- Última fecha de compra/entrada por producto
        fecha_base AS (
            SELECT 
                inv."Autonumerico",
                mov."Empresa",
                MAX(mov."Fecha") as max_fecha
            FROM "public"."Vista_Auxiliar_Movimientos_Inventario" mov
            INNER JOIN "public"."Vista_Tabla_Inventarios" inv 
                ON mov."CodigoInventario" = inv."Codigo_Producto"
            WHERE mov."Tipo_Documento" IN ('FC')
            GROUP BY inv."Autonumerico", mov."Empresa"
        ),
        
        -- Costos base
        base_costos AS (
            SELECT DISTINCT ON (inv."Codigo_Producto", mov."Empresa")
                mov."Nombre_Documento" || ' ' || COALESCE(CAST(mov."prefijo" AS TEXT), '') || ' ' || mov."Numero_Documento" as num_doc,
                mov."Tercero" as proveedor,
                COALESCE(CAST(mov."Valor_Unitario" AS NUMERIC), 0) as val_unit,
                COALESCE(CAST(mov."Valor_Unitario" AS NUMERIC), 0) * (COALESCE(CAST(mov."Descuento_Porcentaje" AS NUMERIC), 0) / 100) as val_dcto,
                (COALESCE(CAST(mov."Valor_Unitario" AS NUMERIC), 0) - 
                 COALESCE(CAST(mov."Valor_Unitario" AS NUMERIC), 0) * (COALESCE(CAST(mov."Descuento_Porcentaje" AS NUMERIC), 0) / 100)) * 
                 (1 + COALESCE(CAST(mov."Iva" AS NUMERIC), 0) / 100) as val_neto,
                inv."Codigo_Producto",
                fb.max_fecha,
                mov."Empresa",
                mov."Identificacion_Tercero" as identificacion_tercero
            FROM "public"."Vista_Auxiliar_Movimientos_Inventario" mov
            INNER JOIN fecha_base fb ON mov."Fecha" = fb.max_fecha AND mov."Empresa" = fb."Empresa"
            INNER JOIN "public"."Vista_Tabla_Inventarios" inv 
                ON mov."CodigoInventario" = inv."Codigo_Producto" 
                AND fb."Autonumerico" = inv."Autonumerico"
            WHERE mov."Tipo_Documento" IN ('FC')
              AND COALESCE(CAST(mov."Anulado" AS INTEGER), 0) = 0
            ORDER BY inv."Codigo_Producto", mov."Empresa", mov."Fecha" DESC
        ),
        
        -- Existencias por empresa IMPERIO
        existencias_mc AS (
            SELECT 
                inv."Codigo_Producto",
                COALESCE(SUM(COALESCE(CAST(ex."Existencia" AS NUMERIC), 0)), 0) as exist_mc
            FROM "public"."Vista_Existencias" ex
            INNER JOIN "public"."Vista_Tabla_Inventarios" inv ON ex."IdInventario" = inv."Autonumerico"
            WHERE inv."Empresa" = 'IMPERIO'
            GROUP BY inv."Codigo_Producto"
        )
        
        -- Consulta final AGRUPADA
        SELECT 
            inv."Empresa" as empresa,
            bc.max_fecha as fecha,
            bc.num_doc,
            MAX(pp.prov1_nombre) as proveedor,
            MAX(pp.prov1_identificacion) as identificacion_tercero,
            inv."Descripcion_Grupo_Tres" as grupo3,
            inv."Descripcion_Grupo_Cuatro" as grupo4,
            inv."Descripcion_Grupo_Cinco" as grupo5,
            inv."Codigo_Producto" as cod_prod,
            inv."Descripcion" as descripcion,
            inv."Unidad_de_Medida" as unidad_medida,
            -- SUMAR exist y exist_mc
            SUM(COALESCE(CAST(ex."Existencia" AS NUMERIC), 0)) as exist,
            MAX(COALESCE(emc.exist_mc, 0)) as exist_mc,
            MAX(COALESCE(vaa.cantidad, 0)) as cantidad_ventas_anterior,
            MAX(COALESCE(vac.cantidad, 0)) as cantidad_ventas_actual,
            -- Fórmula de sugerido: 2 × (ventas / días) × dias_entrega
            MAX(CASE 
                WHEN dp.dias > 0 AND COALESCE(mde.dias_entrega, 5) > 0 THEN
                    2 * (COALESCE(v.ventas, 0) / dp.dias) * COALESCE(mde.dias_entrega, 5)
                ELSE 
                    COALESCE(vaa.cantidad, 0) / 12
            END) as sugerido_compras,
            0 as cantidad_a_pedir,
            MAX(pp.prov1) as proveedor1,
            MAX(pp.prov2) as proveedor2,
            MAX(pp.prov3) as proveedor3,
            MAX(pp.prov4) as proveedor4,
            MAX(COALESCE(c.compras, 0)) as compras_en_el_periodo,
            MAX(COALESCE(e.entradas, 0)) as total_entradas_en_el_periodo,
            MAX(c.max_fecha_fc) as ultima_fecha_compra,
            MAX(COALESCE(v.ventas, 0)) as ventas_en_el_periodo,
            MAX(COALESCE(s.salidas, 0)) as total_salidas_en_el_periodo,
            MAX(v.max_fecha_fv) as ultima_fecha_venta,
            MAX(COALESCE(c.compras, 0) - COALESCE(v.ventas, 0)) as saldo_actual,
            MAX(COALESCE(bc.val_unit, 0)) as val_unit,
            MAX(COALESCE(bc.val_dcto, 0)) as dcto,
            MAX(COALESCE(bc.val_neto, 0)) as val_neto,
            MAX(COALESCE(CAST(inv."Precio1" AS NUMERIC), 0)) as precio1,
            MAX(CASE WHEN COALESCE(CAST(inv."Precio1" AS NUMERIC), 0) = 0 THEN 0 
                 ELSE ((COALESCE(CAST(inv."Precio1" AS NUMERIC), 0) - COALESCE(bc.val_neto, 0)) / COALESCE(CAST(inv."Precio1" AS NUMERIC), 1)) * 100 
            END) as util_1,
            MAX(COALESCE(CAST(inv."Precio2" AS NUMERIC), 0)) as precio2,
            MAX(CASE WHEN COALESCE(CAST(inv."Precio2" AS NUMERIC), 0) = 0 THEN 0 
                 ELSE ((COALESCE(CAST(inv."Precio2" AS NUMERIC), 0) - COALESCE(bc.val_neto, 0)) / COALESCE(CAST(inv."Precio2" AS NUMERIC), 1)) * 100 
            END) as util_2,
            MAX(COALESCE(mde.dias_entrega, 0)) as dias_entrega_usado
        FROM "public"."Vista_Tabla_Inventarios" inv
        CROSS JOIN dias_periodo dp
        LEFT JOIN "public"."Vista_Existencias" ex ON ex."IdInventario" = inv."Autonumerico" AND ex."Empresa" = inv."Empresa"
        LEFT JOIN base_costos bc ON bc."Codigo_Producto" = inv."Codigo_Producto" AND bc."Empresa" = inv."Empresa"
        LEFT JOIN ventas v ON v."CodigoInventario" = inv."Codigo_Producto" AND v."Empresa" = bc."Empresa"
        LEFT JOIN ventas_anio_anterior vaa ON vaa."CodigoInventario" = inv."Codigo_Producto" AND vaa."Empresa" = bc."Empresa"
        LEFT JOIN ventas_anio_actual vac ON vac."CodigoInventario" = inv."Codigo_Producto" AND vac."Empresa" = bc."Empresa"
        LEFT JOIN compras c ON c."CodigoInventario" = inv."Codigo_Producto" AND c."Empresa" = bc."Empresa"
        LEFT JOIN entradas e ON e."CodigoInventario" = inv."Codigo_Producto" AND e."Empresa" = bc."Empresa"
        LEFT JOIN salidas s ON s."CodigoInventario" = inv."Codigo_Producto" AND s."Empresa" = bc."Empresa"
        LEFT JOIN prov_pivot pp ON pp."CodigoInventario" = inv."Codigo_Producto" AND pp."Empresa" = inv."Empresa"
        LEFT JOIN existencias_mc emc ON emc."Codigo_Producto" = inv."Codigo_Producto"
        LEFT JOIN min_dias_entrega mde ON mde.empresa = bc."Empresa" AND mde.nit_proveedor = bc.identificacion_tercero
        WHERE inv."Clasificacion" = 'Producto'
          AND COALESCE(v.ventas, 0) <> 0
          AND NOT EXISTS (
              SELECT 1 FROM "public".inventario_excluido ie 
              WHERE ie.codigo_producto = inv."Codigo_Producto" 
                AND ie.empresa = bc."Empresa"
                AND ie.status = true
          )
          {filtro_grupo3}
          {filtro_grupo4}
          {filtro_grupo5}
        -- GROUP BY con todos los campos no agregados
        GROUP BY 
            inv."Empresa",
            bc.max_fecha,
            bc.num_doc,
            inv."Descripcion_Grupo_Tres",
            inv."Descripcion_Grupo_Cuatro",
            inv."Descripcion_Grupo_Cinco",
            inv."Codigo_Producto",
            inv."Descripcion",
            inv."Unidad_de_Medida"
        ORDER BY proveedor DESC
        """)
        
        # Ejecutar la query con bindparams explícitos
        params = [
            bindparam("fecha_inicial", value=fecha_inicial),
            bindparam("fecha_final", value=fecha_final)
        ]
        
        # Agregar parámetros de grupo solo si se proporcionaron
        if grupo3:
            params.append(bindparam("grupo3", value=grupo3))
        if grupo4:
            params.append(bindparam("grupo4", value=grupo4))
        if grupo5:
            params.append(bindparam("grupo5", value=grupo5))
        
        query = query.bindparams(*params)
        
        # Log de la consulta con todos los filtros y parámetros
        logger.info("=" * 80)
        logger.info("CONSULTA SUGERIDO DE COMPRAS - Query con filtros aplicados")
        logger.info("=" * 80)
        logger.info(f"Parámetros:")
        logger.info(f"  - fecha_inicial: {fecha_inicial}")
        logger.info(f"  - fecha_final: {fecha_final}")
        logger.info(f"  - grupo3: {grupo3 if grupo3 else 'No especificado'}")
        logger.info(f"  - grupo4: {grupo4 if grupo4 else 'No especificado'}")
        logger.info(f"  - grupo5: {grupo5 if grupo5 else 'No especificado'}")
        logger.info("-" * 80)
        logger.info("Query SQL completa:")
        logger.info(str(query))
        logger.info("=" * 80)
        
        result = await self.db.execute(query)
        rows = result.fetchall()
        
        logger.info(f"Registros obtenidos de la consulta: {len(rows)}")
        logger.info("=" * 80)
        
        # Crear los registros en la tabla sugerido_compras
        items_to_create = []
        for row in rows:
            item = SugeridoComprasCreate(
                empresa=row.empresa or "",
                fecha=row.fecha,
                num_doc=row.num_doc,
                proveedor=row.proveedor,
                identificacion_tercero=row.identificacion_tercero,
                grupo3=row.grupo3,
                grupo4=row.grupo4,
                grupo5=row.grupo5,
                cod_prod=row.cod_prod,
                descripcion=row.descripcion,
                unidad_medida=row.unidad_medida,
                exist=Decimal(str(row.exist)) if row.exist else Decimal("0"),
                exist_mc=Decimal(str(row.exist_mc)) if row.exist_mc else Decimal("0"),
                cantidad_ventas_anterior=Decimal(str(row.cantidad_ventas_anterior)) if row.cantidad_ventas_anterior else Decimal("0"),
                cantidad_ventas_actual=Decimal(str(row.cantidad_ventas_actual)) if row.cantidad_ventas_actual else Decimal("0"),
                sugerido_compras=Decimal(str(row.sugerido_compras)) if row.sugerido_compras else Decimal("0"),
                cantidad_a_pedir=Decimal(str(math.ceil(float(row.sugerido_compras)))) if row.sugerido_compras else Decimal("0"),
                proveedor1=row.proveedor1,
                proveedor2=row.proveedor2,
                proveedor3=row.proveedor3,
                proveedor4=row.proveedor4,
                compras_en_el_periodo=Decimal(str(row.compras_en_el_periodo)) if row.compras_en_el_periodo else Decimal("0"),
                total_entradas_en_el_periodo=Decimal(str(row.total_entradas_en_el_periodo)) if row.total_entradas_en_el_periodo else Decimal("0"),
                ultima_fecha_compra=row.ultima_fecha_compra,
                ventas_en_el_periodo=Decimal(str(row.ventas_en_el_periodo)) if row.ventas_en_el_periodo else Decimal("0"),
                total_salidas_en_el_periodo=Decimal(str(row.total_salidas_en_el_periodo)) if row.total_salidas_en_el_periodo else Decimal("0"),
                ultima_fecha_venta=row.ultima_fecha_venta,
                saldo_actual=Decimal(str(row.saldo_actual)) if row.saldo_actual else Decimal("0"),
                val_unit=Decimal(str(row.val_unit)) if row.val_unit else Decimal("0"),
                dcto=Decimal(str(row.dcto)) if row.dcto else Decimal("0"),
                val_neto=Decimal(str(row.val_neto)) if row.val_neto else Decimal("0"),
                precio1=Decimal(str(row.precio1)) if row.precio1 else Decimal("0"),
                util_1=Decimal(str(row.util_1)) if row.util_1 else Decimal("0"),
                precio2=Decimal(str(row.precio2)) if row.precio2 else Decimal("0"),
                util_2=Decimal(str(row.util_2)) if row.util_2 else Decimal("0"),
                status=StatusSugerido.Created
            )
            items_to_create.append(item)
        
        # Insertar en la base de datos
        if items_to_create:
            await self.bulk_create(items_to_create)
        
        # Retornar los registros con status = Created
        return await self.get_by_status(StatusSugerido.Created)

    async def get_reporte(
        self,
        fecha_inicial: date,
        fecha_final: date,
        identificacion_tercero: Optional[str] = None,
        status_filter: Optional[str] = None
    ) -> List[dict]:
        """
        Obtener reporte de sugerido de compras filtrado por rango de fechas en updated_at,
        opcionalmente por identificacion_tercero y status.
        """
        from datetime import datetime, timedelta
        
        # Convertir fechas a datetime para comparar con updated_at (que es timestamp)
        fecha_inicio_dt = datetime.combine(fecha_inicial, datetime.min.time())
        fecha_fin_dt = datetime.combine(fecha_final, datetime.max.time())
        
        query = select(
            SugeridoComprasModel.empresa,
            SugeridoComprasModel.proveedor,
            SugeridoComprasModel.cod_prod,
            SugeridoComprasModel.descripcion,
            SugeridoComprasModel.unidad_medida,
            SugeridoComprasModel.cantidad_proveedor,
            SugeridoComprasModel.valor_unitario_proveedor,
            SugeridoComprasModel.tipo_doc_exp,
            SugeridoComprasModel.prefijo_exp,
            SugeridoComprasModel.num_doc_exp,
            SugeridoComprasModel.updated_at
        ).where(
            and_(
                SugeridoComprasModel.updated_at >= fecha_inicio_dt,
                SugeridoComprasModel.updated_at <= fecha_fin_dt
            )
        )
        
        if identificacion_tercero:
            query = query.where(
                SugeridoComprasModel.identificacion_tercero == identificacion_tercero
            )
        
        if status_filter:
            query = query.where(
                SugeridoComprasModel.status == ModelStatusSugerido(status_filter)
            )
        
        query = query.order_by(SugeridoComprasModel.updated_at.desc())
        
        result = await self.db.execute(query)
        rows = result.fetchall()
        
        return [
            {
                "empresa": row.empresa,
                "proveedor": row.proveedor,
                "cod_prod": row.cod_prod,
                "descripcion": row.descripcion,
                "unidad_medida": row.unidad_medida,
                "cantidad_proveedor": row.cantidad_proveedor,
                "valor_unitario_proveedor": row.valor_unitario_proveedor,
                "tipo_doc_exp": row.tipo_doc_exp,
                "prefijo_exp": row.prefijo_exp,
                "num_doc_exp": row.num_doc_exp,
                "updated_at": row.updated_at
            }
            for row in rows
        ]
