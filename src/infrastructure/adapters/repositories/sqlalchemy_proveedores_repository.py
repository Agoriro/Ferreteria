"""
Implementación SQLAlchemy del repositorio de proveedores (dropdown).
Consulta Vista_Auxiliar_Terceros donde Propiedades contiene 'Proveedor'.
"""
from typing import List, Tuple

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from domain.ports.proveedores_repository import ProveedoresRepositoryPort


class SQLAlchemyProveedoresRepository(ProveedoresRepositoryPort):
    """Adaptador de persistencia para proveedores usando Vista_Auxiliar_Terceros."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_proveedores_dropdown(self) -> List[Tuple[str, str]]:
        """Lista proveedores para dropdown: (identificacion, nombre_completo)."""
        query = text("""
            SELECT 
                "Identificacion",
                MAX(TRIM(
                    CONCAT_WS(' ',
                        "Primer_Nombre",
                        "Segundo_Nombre",
                        "Primer_Apellido",
                        "Segundo_Apellido"
                    )
                )) AS "Nombre_Completo"
            FROM "public"."Vista_Auxiliar_Terceros"
            WHERE "Propiedades" LIKE '%Proveedor%'
            GROUP BY "Identificacion"
            ORDER BY "Nombre_Completo"
        """)
        result = await self.session.execute(query)
        rows = result.fetchall()
        return [(r[0] or "", r[1] or "") for r in rows]
