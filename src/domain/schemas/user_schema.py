"""
DTOs para User - Principio SOLID: Interface Segregation.
Diferentes interfaces para diferentes operaciones.
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    nombres: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=100)
    id_proveedor: Optional[int] = None


class UserCreate(UserBase):
    """DTO para creación de usuario."""
    password: str = Field(..., min_length=8)
    rol_id: int = Field(..., gt=0)


class UserUpdate(BaseModel):
    """DTO para actualización - todos los campos opcionales."""
    nombres: Optional[str] = Field(None, min_length=1, max_length=100)
    apellidos: Optional[str] = Field(None, min_length=1, max_length=100)
    id_proveedor: Optional[int] = None
    estado: Optional[bool] = None
    rol_id: Optional[int] = Field(None, gt=0)


class UserChangePassword(BaseModel):
    """DTO para cambio de contraseña."""
    current_password: str
    new_password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    """DTO para respuesta."""
    id: int
    estado: bool
    rol_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class UserWithRole(UserResponse):
    """DTO con información del rol."""
    rol_nombre: str
