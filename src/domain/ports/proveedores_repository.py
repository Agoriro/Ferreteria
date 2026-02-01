"""
Puerto para repositorio de proveedores (Vista_Auxiliar_Terceros).
"""
from abc import ABC, abstractmethod
from typing import List, Tuple


class ProveedoresRepositoryPort(ABC):
    """Interface para consulta de proveedores (dropdown)."""

    @abstractmethod
    async def get_proveedores_dropdown(self) -> List[Tuple[str, str]]:
        """
        Lista proveedores para lista desplegable.

        Returns:
            Lista de tuplas (identificacion, nombre_completo).
        """
        pass
