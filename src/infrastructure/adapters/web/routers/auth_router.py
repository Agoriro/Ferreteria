"""
Router para autenticación (Adaptador Web).
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from domain.schemas.auth_schema import Token, LoginRequest, RefreshTokenRequest
from application.use_cases.auth_use_case import AuthUseCase
from infrastructure.adapters.web.dependencies import get_auth_use_case

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_use_case: AuthUseCase = Depends(get_auth_use_case)
):
    """
    Endpoint de login - Retorna Access Token y Refresh Token.
    """
    login_data = LoginRequest(username=form_data.username, password=form_data.password)
    return await auth_use_case.login(login_data)


@router.post("/refresh-token", response_model=Token)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    auth_use_case: AuthUseCase = Depends(get_auth_use_case)
):
    """
    Endpoint para renovar Access Token usando Refresh Token.
    """
    return await auth_use_case.refresh_access_token(refresh_data.refresh_token)
