"""
Puerto (Interface) para repositorio de Vista_Tabla_Inventarios.
Principio SOLID: Dependency Inversion - Dependemos de abstracción, no implementación.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple


class VistaInventariosRepositoryPort(ABC):
    """Interface que define el contrato para consulta de inventarios."""
    
    @abstractmethod
    async def get_all_basic(
        self, 
        skip: int = 0, 
        limit: int = 100,
        empresa: str = None
    ) -> Tuple[List, int]:
        """
        Lista todos los inventarios con campos básicos (empresa, codigo_producto, descripcion).
        
        Args:
            skip: Número de registros a saltar para paginación
            limit: Número máximo de registros a retornar
            empresa: Filtro opcional por empresa
            
        Returns:
            Tupla con lista de registros y total de registros
        """
        pass

