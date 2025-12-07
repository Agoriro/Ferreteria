"""
DTOs para autenticación.
"""
from pydantic import BaseModel


class Token(BaseModel):
    """Respuesta de login."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Datos dentro del token."""
    username: str
    user_id: int


class LoginRequest(BaseModel):
    """Solicitud de login."""
    username: str
    password: str


class RefreshTokenRequest(BaseModel):
    """Solicitud de refresh token."""
    refresh_token: str
