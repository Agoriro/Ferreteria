"""
Casos de uso de Autenticación.
"""
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from domain.ports.user_repository import UserRepositoryPort
from domain.schemas.auth_schema import LoginRequest, Token
from application.services.password_service import PasswordService
from infrastructure.security.jwt_handler import JWTHandler


class AuthUseCase:
    """Casos de uso para autenticación."""
    
    def __init__(self, user_repository: UserRepositoryPort, jwt_handler: JWTHandler):
        self.user_repository = user_repository
        self.jwt_handler = jwt_handler
        self.password_service = PasswordService()
    
    async def login(self, login_data: LoginRequest) -> Token:
        """Autentica usuario y genera tokens."""
        # Buscar usuario
        user = await self.user_repository.get_by_username(login_data.username)
        
        if not user or not self.password_service.verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar que esté activo
        if not user.estado:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo"
            )
        
        # Generar tokens
        access_token = self.jwt_handler.create_access_token(
            data={"sub": user.username, "user_id": user.id}
        )
        refresh_token = self.jwt_handler.create_refresh_token(
            data={"sub": user.username, "user_id": user.id}
        )
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token
        )
    
    async def refresh_access_token(self, refresh_token: str) -> Token:
        """Genera nuevo access token desde refresh token."""
        payload = self.jwt_handler.verify_token(refresh_token)
        
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado"
            )
        
        username = payload.get("sub")
        user_id = payload.get("user_id")
        
        # Generar nuevo access token
        new_access_token = self.jwt_handler.create_access_token(
            data={"sub": username, "user_id": user_id}
        )
        
        return Token(
            access_token=new_access_token,
            refresh_token=refresh_token  # Mismo refresh token
        )
