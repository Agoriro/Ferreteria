"""
Casos de uso de Roles.
"""
from fastapi import HTTPException, status
from domain.ports.role_repository import RoleRepositoryPort
from domain.schemas.role_schema import RoleCreate, RoleUpdate


class RoleUseCase:
    """Casos de uso para gestión de roles."""
    
    def __init__(self, role_repository: RoleRepositoryPort):
        self.role_repository = role_repository
    
    async def create_role(self, role_data: RoleCreate):
        """Crea un nuevo rol."""
        existing = await self.role_repository.get_by_name(role_data.nombre_rol)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El rol ya existe"
            )
        
        return await self.role_repository.create(role_data)
    
    async def get_role_by_id(self, role_id: int):
        """Obtiene rol por ID."""
        role = await self.role_repository.get_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )
        return role
    
    async def get_all_roles(self):
        """Lista todos los roles."""
        return await self.role_repository.get_all()
    
    async def update_role(self, role_id: int, role_data: RoleUpdate):
        """Actualiza un rol."""
        role = await self.role_repository.get_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )
        
        return await self.role_repository.update(role_id, role_data)
