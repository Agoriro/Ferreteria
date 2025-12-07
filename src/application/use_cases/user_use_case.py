"""
Casos de uso de Usuario - Lógica de negocio.
Principio SOLID: Open/Closed - Abierto a extensión, cerrado a modificación.
"""
from typing import List
from fastapi import HTTPException, status
from domain.ports.user_repository import UserRepositoryPort
from domain.schemas.user_schema import UserCreate, UserUpdate, UserChangePassword
from application.services.password_service import PasswordService


class UserUseCase:
    """
    Casos de uso para gestión de usuarios.
    Principio SOLID: Dependency Inversion - Depende de puerto, no de implementación.
    """
    
    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository
        self.password_service = PasswordService()
    
    async def create_user(self, user_data: UserCreate):
        """Crea un nuevo usuario."""
        # Validar que username no exista
        existing_user = await self.user_repository.get_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El username ya está registrado"
            )
        
        # Hash password
        hashed_password = self.password_service.hash_password(user_data.password)
        
        # Crear usuario
        return await self.user_repository.create(user_data, hashed_password)
    
    async def get_user_by_id(self, user_id: int):
        """Obtiene usuario por ID."""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return user
    
    async def get_all_users(self, skip: int = 0, limit: int = 100, include_inactive: bool = False):
        """Lista todos los usuarios."""
        return await self.user_repository.get_all(skip, limit, include_inactive)
    
    async def update_user(self, user_id: int, user_data: UserUpdate):
        """Actualiza un usuario."""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        return await self.user_repository.update(user_id, user_data)
    
    async def delete_user(self, user_id: int):
        """Soft delete de usuario."""
        success = await self.user_repository.soft_delete(user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return {"message": "Usuario eliminado exitosamente"}
    
    async def change_password(self, user_id: int, password_data: UserChangePassword):
        """Cambia la contraseña de un usuario."""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar contraseña actual
        if not self.password_service.verify_password(password_data.current_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contraseña actual incorrecta"
            )
        
        # Hash nueva contraseña
        new_hashed = self.password_service.hash_password(password_data.new_password)
        
        await self.user_repository.update_password(user_id, new_hashed)
        return {"message": "Contraseña actualizada exitosamente"}
