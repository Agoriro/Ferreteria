"""
Casos de uso para proveedores (dropdown desde Vista_Auxiliar_Terceros).
"""
from typing import List

from domain.ports.proveedores_repository import ProveedoresRepositoryPort
from domain.schemas.proveedores_schema import ProveedorDropdownItem


class ProveedoresUseCase:
    """Casos de uso para listado de proveedores."""

    def __init__(self, repository: ProveedoresRepositoryPort):
        self.repository = repository

    async def get_proveedores_dropdown(self) -> List[ProveedorDropdownItem]:
        """Lista proveedores para lista desplegable (identificacion, nombre_completo)."""
        rows = await self.repository.get_proveedores_dropdown()
        return [
            ProveedorDropdownItem(identificacion=ident, nombre_completo=nombre)
            for ident, nombre in rows
        ]
