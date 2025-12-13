"""
Modelos SQLAlchemy (Adaptadores de persistencia).
Estos son detalles de implementación, no dominio.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from infrastructure.config.database import Base


class RoleModel(Base):
    __tablename__ = "roles"
    
    id_rol = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    usuarios = relationship("UserModel", back_populates="rol")
    permisos = relationship("DetallePermisoModel", back_populates="rol")


class FormularioModel(Base):
    __tablename__ = "formularios"
    
    id_formulario = Column(Integer, primary_key=True, index=True)
    nombre_formulario = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String, nullable=True)
    ruta = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    permisos = relationship("DetallePermisoModel", back_populates="formulario")


class DetallePermisoModel(Base):
    __tablename__ = "detalle_permisos"
    
    id_permiso = Column(Integer, primary_key=True, index=True)
    id_rol = Column(Integer, ForeignKey("roles.id_rol", ondelete="CASCADE"), nullable=False)
    id_formulario = Column(Integer, ForeignKey("formularios.id_formulario", ondelete="CASCADE"), nullable=False)
    puede_leer = Column(Boolean, default=True)
    puede_crear = Column(Boolean, default=False)
    puede_editar = Column(Boolean, default=False)
    puede_eliminar = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    rol = relationship("RoleModel", back_populates="permisos")
    formulario = relationship("FormularioModel", back_populates="permisos")


class UserModel(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    id_proveedor = Column(Integer, nullable=True)
    estado = Column(Boolean, default=True, index=True)
    rol_id = Column(Integer, ForeignKey("roles.id_rol"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    rol = relationship("RoleModel", back_populates="usuarios")
    refresh_tokens = relationship("RefreshTokenModel", back_populates="user", cascade="all, delete-orphan")


class RefreshTokenModel(Base):
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(500), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    revoked = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("UserModel", back_populates="refresh_tokens")


class InventarioExcluidoModel(Base):
    """Modelo para productos excluidos del inventario."""
    __tablename__ = "inventario_excluido"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    codigo_producto = Column(String(100), nullable=False, index=True)
    status = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
