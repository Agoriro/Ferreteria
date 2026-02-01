"""
Aplicación principal FastAPI.
Punto de entrada que ensambla todos los adaptadores.
"""
import traceback
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from infrastructure.config.settings import get_settings
from infrastructure.adapters.web.routers import auth_router, user_router, role_router, inventario_excluido_router, dias_entrega_proveedor_router, vista_inventarios_router, sugerido_compras_router, grupos_router, proveedores_router, permiso_router

settings = get_settings()

# Crear aplicación
app = FastAPI(
    title=settings.APP_NAME,
    description="API de autenticación con Arquitectura Hexagonal",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS - Orígenes permitidos (desde variable de entorno o defaults)
origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Manejador global de excepciones - muestra errores en consola
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Captura todos los errores y los muestra en consola."""
    print("=" * 50)
    print(f"ERROR en {request.method} {request.url}")
    print(f"Tipo: {type(exc).__name__}")
    print(f"Mensaje: {str(exc)}")
    print("Traceback:")
    traceback.print_exc()
    print("=" * 50)
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
            "type": type(exc).__name__
        }
    )


# Incluir routers
app.include_router(auth_router.router, prefix="/api/v1")
app.include_router(user_router.router, prefix="/api/v1")
app.include_router(role_router.router, prefix="/api/v1")
app.include_router(inventario_excluido_router.router, prefix="/api/v1")
app.include_router(dias_entrega_proveedor_router.router, prefix="/api/v1")
app.include_router(vista_inventarios_router.router, prefix="/api/v1")
app.include_router(sugerido_compras_router.router, prefix="/api/v1")
app.include_router(grupos_router.router, prefix="/api/v1")
app.include_router(proveedores_router.router, prefix="/api/v1")
app.include_router(permiso_router.router, prefix="/api/v1")


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
