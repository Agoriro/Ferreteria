"""
Aplicación principal FastAPI.
Punto de entrada que ensambla todos los adaptadores.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.config.settings import get_settings
from infrastructure.adapters.web.routers import auth_router, user_router, role_router, inventario_excluido_router, dias_entrega_proveedor_router, vista_inventarios_router

settings = get_settings()

# Crear aplicación
app = FastAPI(
    title=settings.APP_NAME,
    description="API de autenticación con Arquitectura Hexagonal",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configurar según necesidad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth_router.router, prefix="/api/v1")
app.include_router(user_router.router, prefix="/api/v1")
app.include_router(role_router.router, prefix="/api/v1")
app.include_router(inventario_excluido_router.router, prefix="/api/v1")
app.include_router(dias_entrega_proveedor_router.router, prefix="/api/v1")
app.include_router(vista_inventarios_router.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Health check."""
    return {
        "message": "API funcionando correctamente",
        "version": "1.0.0",
        "architecture": "Hexagonal (Ports & Adapters)"
    }


@app.get("/health")
async def health_check():
    """Endpoint de salud."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
