"""
Configuración de base de datos con SQLAlchemy 2.0 (async).
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from .settings import get_settings

settings = get_settings()

# Motor asíncrono
engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    Dependency para obtener sesión de BD.
    Principio SOLID: Dependency Inversion - Inyección de dependencias.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
