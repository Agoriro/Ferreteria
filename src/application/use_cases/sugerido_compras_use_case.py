"""
Casos de uso para Sugerido de Compras.
"""
from typing import List, Optional
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal
from collections import defaultdict
from fastapi import HTTPException, status

from domain.ports.sugerido_compras_repository import SugeridoComprasRepositoryPort
from domain.schemas.sugerido_compras_schema import (
    SugeridoComprasCreate,
    SugeridoComprasUpdate,
    SugeridoComprasResponse,
    SugeridoComprasListResponse,
    StatusSugerido,
    GenerarSugeridoRequest,
    SugeridoProcessedResponse,
    SugeridoProcessedListResponse,
    OrdenCompra,
    OrdenCompraEncabezado,
    OrdenCompraDetalle
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
    
    async def bulk_update_created_to_requested(self) -> dict:
        """
        Actualizar todos los registros con status 'Created' a 'Requested'.
        """
        updated_count = await self.repository.bulk_update_created_to_requested()
        if updated_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron registros con status 'Created'"
            )
        return {"message": f"{updated_count} registros actualizados a 'Requested'", "updated_count": updated_count}
    
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
    
    async def get_requested_by_tercero(self, identificacion_tercero: Optional[str] = None) -> SugeridoComprasListResponse:
        """
        Obtener registros con status 'Requested'.
        Si se proporciona identificacion_tercero, filtra por ese valor.
        """
        items = await self.repository.get_requested_by_tercero(identificacion_tercero)
        return SugeridoComprasListResponse(items=items, total=len(items))
    
    async def bulk_update_proveedor(self, items: List[dict]) -> dict:
        """
        Actualizar cantidad_proveedor, valor_unitario_proveedor y cambiar status a 'Processed'.
        Retorna información sobre los registros actualizados.
        """
        if not items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe proporcionar al menos un item para actualizar"
            )
        
        updated_ids = await self.repository.bulk_update_proveedor(items)
        
        return {
            "message": "Registros actualizados correctamente",
            "updated_count": len(updated_ids),
            "updated_ids": [str(uid) for uid in updated_ids]
        }
    
    async def get_processed(self) -> SugeridoProcessedListResponse:
        """
        Obtener registros con status 'Processed' con campos reducidos.
        """
        items_dict = await self.repository.get_processed()
        items = [SugeridoProcessedResponse(**item) for item in items_dict]
        return SugeridoProcessedListResponse(items=items, total=len(items))
    
    async def bulk_update_to_exported(self, ids: List[UUID]) -> dict:
        """
        Actualizar múltiples registros a status 'Exported' y generar órdenes de compra.
        """
        if not ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe proporcionar al menos un ID para actualizar"
            )
        
        # 1. Obtener registros completos antes de actualizar
        sugeridos = await self.repository.get_sugeridos_for_export(ids)
        
        if not sugeridos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron registros con los IDs proporcionados"
            )
        
        # 2. Obtener máximo número de documento OC
        max_doc = await self.repository.get_max_documento_oc()
        
        # 3. Obtener IVA de productos
        cod_prods = list(set(s["cod_prod"] for s in sugeridos))
        iva_map = await self.repository.get_productos_iva(cod_prods)
        
        # 4. Agrupar por empresa + identificacion_tercero
        grupos = defaultdict(list)
        for sug in sugeridos:
            key = (sug["empresa"], sug["identificacion_tercero"])
            grupos[key].append(sug)
        
        # 5. Generar órdenes de compra
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        ordenes = []
        doc_counter = 1
        doc_info_map = {}
        
        for (empresa, identificacion_tercero), items in grupos.items():
            # Encabezado
            tipo_doc = "OC"
            prefijo = "CO"
            num_doc = str(max_doc + doc_counter)
            
            encabezado = OrdenCompraEncabezado(
                empresa=empresa or "",
                tipo_documento=tipo_doc,
                prefijo=prefijo,
                documento_numero=num_doc,
                fecha=fecha_actual,
                tercero_interno="39425084",
                tercero_externo=identificacion_tercero or "",
                nota="Orden de compra generada desde la Herramienta Web",
                forma_pago="CREDITO",
                verificado=-1,
                anulado=0
            )
            
            # Detalles
            detalles = []
            for item in items:
                iva = iva_map.get(item["cod_prod"], 0)
                detalle = OrdenCompraDetalle(
                    producto=item["cod_prod"] or "",
                    bodega="Principal",
                    unidad_de_medida=item["unidad_medida"] or "",
                    cantidad=Decimal(str(item["cantidad_proveedor"] or 0)),
                    iva=Decimal(str(round(iva, 2))),
                    valor_unitario=Decimal(str(item["valor_unitario_proveedor"] or 0)),
                    descuento=Decimal("0"),
                    vencimiento=fecha_actual
                )
                detalles.append(detalle)
                
                # Mapear cada registro a los datos del documento
                doc_info_map[item["id"]] = {
                    "tipo_doc": tipo_doc,
                    "prefijo": prefijo,
                    "num_doc": num_doc
                }
            
            orden = OrdenCompra(encabezado=encabezado, detalles=detalles)
            ordenes.append(orden)
            doc_counter += 1
        
        # 6. Actualizar status a Exported y guardar datos del documento
        updated_ids = await self.repository.bulk_update_to_exported(ids, doc_info_map)
        
        return {
            "message": "Registros actualizados a 'Exported' correctamente",
            "updated_count": len(updated_ids),
            "updated_ids": [str(uid) for uid in updated_ids],
            "ordenes_compra": ordenes
        }

    async def get_reporte(
        self,
        fecha_inicial: date,
        fecha_final: date,
        identificacion_tercero: Optional[str] = None,
        status_filter: Optional[str] = None
    ) -> dict:
        """
        Obtener reporte de sugerido de compras filtrado por fechas y filtros opcionales.
        """
        if fecha_final < fecha_inicial:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha final debe ser mayor o igual a la fecha inicial"
            )
        
        items = await self.repository.get_reporte(
            fecha_inicial=fecha_inicial,
            fecha_final=fecha_final,
            identificacion_tercero=identificacion_tercero,
            status_filter=status_filter
        )
        
        return {"items": items, "total": len(items)}

    async def reject(self, id: UUID) -> SugeridoComprasResponse:
        """
        Rechazar un registro de sugerido de compras.
        Solo se puede rechazar un registro con status 'Processed'.
        """
        record = await self.repository.get_by_id(id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Registro con ID {id} no encontrado"
            )
        
        if record.status != StatusSugerido.Processed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Solo se pueden rechazar registros con status 'Processed'. Status actual: '{record.status.value}'"
            )
        
        result = await self.repository.update_status(id, StatusSugerido.Rejected)
        return result
