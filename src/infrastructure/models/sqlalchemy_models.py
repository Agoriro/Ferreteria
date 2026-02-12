"""
Modelos SQLAlchemy (Adaptadores de persistencia).
Estos son detalles de implementación, no dominio.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table, Numeric, SmallInteger, Date, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from infrastructure.config.database import Base

# Definir el schema a usar
SCHEMA = "public"


class RoleModel(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": SCHEMA}
    
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
    __table_args__ = {"schema": SCHEMA}
    
    id_formulario = Column(Integer, primary_key=True, index=True)
    nombre_formulario = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String, nullable=True)
    ruta = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    permisos = relationship("DetallePermisoModel", back_populates="formulario")


class DetallePermisoModel(Base):
    __tablename__ = "detalle_permisos"
    __table_args__ = {"schema": SCHEMA}
    
    id_permiso = Column(Integer, primary_key=True, index=True)
    id_rol = Column(Integer, ForeignKey(f"{SCHEMA}.roles.id_rol", ondelete="CASCADE"), nullable=False)
    id_formulario = Column(Integer, ForeignKey(f"{SCHEMA}.formularios.id_formulario", ondelete="CASCADE"), nullable=False)
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
    __table_args__ = {"schema": SCHEMA}
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    id_proveedor = Column(Integer, nullable=True)
    estado = Column(Boolean, default=True, index=True)
    rol_id = Column(Integer, ForeignKey(f"{SCHEMA}.roles.id_rol"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    rol = relationship("RoleModel", back_populates="usuarios")
    refresh_tokens = relationship("RefreshTokenModel", back_populates="user", cascade="all, delete-orphan")


class RefreshTokenModel(Base):
    __tablename__ = "refresh_tokens"
    __table_args__ = {"schema": SCHEMA}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(f"{SCHEMA}.usuarios.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(500), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    revoked = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("UserModel", back_populates="refresh_tokens")


class InventarioExcluidoModel(Base):
    """Modelo para productos excluidos del inventario."""
    __tablename__ = "inventario_excluido"
    __table_args__ = {"schema": SCHEMA}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    codigo_producto = Column(String(100), nullable=False, index=True)
    empresa = Column(String(100), nullable=False, index=True)
    status = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class DiasEntregaProveedorModel(Base):
    """Modelo para días de entrega configurados por proveedor, producto y empresa."""
    __tablename__ = "dias_entrega_proveedor"
    __table_args__ = {"schema": SCHEMA}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    empresa = Column(String(100), nullable=False, index=True)
    nit_proveedor = Column(String(200), nullable=False, index=True)
    codigo_producto = Column(String(100), nullable=False, index=True)
    dias_entrega = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class VistaTablaInventariosModel(Base):
    """Modelo para Vista_Tabla_Inventarios - Tabla de inventarios con información de productos."""
    __tablename__ = "Vista_Tabla_Inventarios"
    __table_args__ = {"schema": SCHEMA}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empresa = Column(String, nullable=False)
    autonumerico = Column(Integer, nullable=True)
    codigo_producto = Column("Codigo_Producto", String, nullable=False)
    descripcion = Column(String, nullable=False)
    maximo_permitido = Column(Numeric(28, 6), nullable=True)
    minimo_permitido = Column(Numeric(28, 6), nullable=True)
    punto_de_reorden = Column(Numeric(28, 6), nullable=True)
    unidad_de_medida = Column(String, nullable=True)
    precio1 = Column(Numeric(28, 6), nullable=True)
    precio2 = Column(Numeric(28, 6), nullable=True)
    precio3 = Column(Numeric(28, 6), nullable=True)
    precio4 = Column(Numeric(28, 6), nullable=True)
    precio5 = Column(Numeric(28, 6), nullable=True)
    precio6 = Column(Numeric(28, 6), nullable=True)
    precio7 = Column(Numeric(28, 6), nullable=True)
    precio8 = Column(Numeric(28, 6), nullable=True)
    precio9 = Column(Numeric(28, 6), nullable=True)
    precio10 = Column(Numeric(28, 6), nullable=True)
    precio11 = Column(Numeric(28, 6), nullable=True)
    precio12 = Column(Numeric(28, 6), nullable=True)
    precio13 = Column(Numeric(28, 6), nullable=True)
    precio14 = Column(Numeric(28, 6), nullable=True)
    precio15 = Column(Numeric(28, 6), nullable=True)
    precio16 = Column(Numeric(28, 6), nullable=True)
    precio17 = Column(Numeric(28, 6), nullable=True)
    precio18 = Column(Numeric(28, 6), nullable=True)
    precio19 = Column(Numeric(28, 6), nullable=True)
    precio20 = Column(Numeric(28, 6), nullable=True)
    precio21 = Column(Numeric(28, 6), nullable=True)
    precio22 = Column(Numeric(28, 6), nullable=True)
    precio23 = Column(Numeric(28, 6), nullable=True)
    precio24 = Column(Numeric(28, 6), nullable=True)
    precio25 = Column(Numeric(28, 6), nullable=True)
    precio26 = Column(Numeric(28, 6), nullable=True)
    precio27 = Column(Numeric(28, 6), nullable=True)
    precio28 = Column(Numeric(28, 6), nullable=True)
    precio29 = Column(Numeric(28, 6), nullable=True)
    precio30 = Column(Numeric(28, 6), nullable=True)
    iva = Column("Iva", Numeric(28, 6), nullable=True)
    activo = Column(SmallInteger, nullable=True)
    grupo_uno = Column(Integer, nullable=True)
    grupo_dos = Column(Integer, nullable=True)
    grupo_tres = Column(Integer, nullable=True)
    grupo_cuatro = Column(Integer, nullable=True)
    grupo_cinco = Column(Integer, nullable=True)
    grupo_seis = Column(Integer, nullable=True)
    grupo_siete = Column(Integer, nullable=True)
    grupo_ocho = Column(Integer, nullable=True)
    grupo_nueve = Column(Integer, nullable=True)
    grupo_diez = Column(Integer, nullable=True)
    codigo_grupo_uno = Column(String, nullable=True)
    descripcion_grupo_uno = Column(String, nullable=True)
    codigo_grupo_dos = Column(String, nullable=True)
    descripcion_grupo_dos = Column(String, nullable=True)
    codigo_grupo_tres = Column(String, nullable=True)
    descripcion_grupo_tres = Column(String, nullable=True)
    codigo_grupo_cuatro = Column(String, nullable=True)
    descripcion_grupo_cuatro = Column(String, nullable=True)
    codigo_grupo_cinco = Column(String, nullable=True)
    descripcion_grupo_cinco = Column(String, nullable=True)
    codigo_grupo_seis = Column(String, nullable=True)
    descripcion_grupo_seis = Column(String, nullable=True)
    codigo_grupo_siete = Column(String, nullable=True)
    descripcion_grupo_siete = Column(String, nullable=True)
    codigo_grupo_ocho = Column(String, nullable=True)
    descripcion_grupo_ocho = Column(String, nullable=True)
    codigo_grupo_nueve = Column(String, nullable=True)
    descripcion_grupo_nueve = Column(String, nullable=True)
    codigo_grupo_diez = Column(String, nullable=True)
    descripcion_grupo_diez = Column(String, nullable=True)
    observaciones = Column(String, nullable=True)
    producto_en_proceso = Column(SmallInteger, nullable=True)
    pertenece_a_un_producto = Column(SmallInteger, nullable=True)
    facturar_sin_existencias = Column(SmallInteger, nullable=True)
    personalizado1 = Column(String, nullable=True)
    personalizado2 = Column(String, nullable=True)
    personalizado3 = Column(String, nullable=True)
    personalizado4 = Column(String, nullable=True)
    personalizado5 = Column(String, nullable=True)
    personalizado6 = Column(String, nullable=True)
    personalizado7 = Column(String, nullable=True)
    personalizado8 = Column(String, nullable=True)
    personalizado9 = Column(String, nullable=True)
    personalizado10 = Column(String, nullable=True)
    personalizado11 = Column(String, nullable=True)
    personalizado12 = Column(String, nullable=True)
    personalizado13 = Column(String, nullable=True)
    personalizado14 = Column(String, nullable=True)
    personalizado15 = Column(String, nullable=True)
    clasificacion = Column(String, nullable=True)
    porcentaje_impoconsumo = Column(Numeric(28, 6), nullable=True)
    valor_impoconsumo = Column(Numeric(28, 6), nullable=True)
    porc_arancel = Column(Numeric(28, 6), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class StatusSugerido(enum.Enum):
    """Enum para el status de sugerido de compras."""
    Created = "Created"
    Requested = "Requested"
    Processed = "Processed"
    Exported = "Exported"


class SugeridoComprasModel(Base):
    """Modelo para Sugerido de Compras."""
    __tablename__ = "sugerido_compras"
    __table_args__ = {"schema": SCHEMA}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    empresa = Column(String(100), nullable=False, index=True)
    fecha = Column(Date, nullable=True)
    num_doc = Column(String(100), nullable=True)
    proveedor = Column(String(255), nullable=True)
    identificacion_tercero = Column(String(100), nullable=True)
    grupo3 = Column(String(255), nullable=True)
    grupo4 = Column(String(255), nullable=True)
    grupo5 = Column(String(255), nullable=True)
    cod_prod = Column(String(100), nullable=False, index=True)
    descripcion = Column(String(500), nullable=True)
    unidad_medida = Column(String(50), nullable=True)
    exist = Column(Numeric(28, 6), default=0)
    exist_mc = Column(Numeric(28, 6), default=0)
    cantidad_ventas_anterior = Column(Numeric(28, 6), default=0)
    cantidad_ventas_actual = Column(Numeric(28, 6), default=0)
    sugerido_compras = Column(Numeric(28, 6), default=0)
    cantidad_a_pedir = Column(Numeric(28, 6), default=0)
    proveedor1 = Column(String(255), nullable=True)
    proveedor2 = Column(String(255), nullable=True)
    proveedor3 = Column(String(255), nullable=True)
    proveedor4 = Column(String(255), nullable=True)
    compras_en_el_periodo = Column(Numeric(28, 6), default=0)
    total_entradas_en_el_periodo = Column(Numeric(28, 6), default=0)
    ultima_fecha_compra = Column(Date, nullable=True)
    ventas_en_el_periodo = Column(Numeric(28, 6), default=0)
    total_salidas_en_el_periodo = Column(Numeric(28, 6), default=0)
    ultima_fecha_venta = Column(Date, nullable=True)
    saldo_actual = Column(Numeric(28, 6), default=0)
    val_unit = Column(Numeric(28, 6), default=0)
    dcto = Column(Numeric(28, 6), default=0)
    val_neto = Column(Numeric(28, 6), default=0)
    precio1 = Column(Numeric(28, 6), default=0)
    util_1 = Column(Numeric(28, 6), default=0)
    precio2 = Column(Numeric(28, 6), default=0)
    util_2 = Column(Numeric(28, 6), default=0)
    cantidad_proveedor = Column(Numeric(28, 6), default=0)
    valor_unitario_proveedor = Column(Numeric(28, 6), default=0)
    tipo_doc_exp = Column(String(100), nullable=True)
    prefijo_exp = Column(String(100), nullable=True)
    num_doc_exp = Column(String(100), nullable=True)
    status = Column(SQLEnum(StatusSugerido, name='status_sugerido', schema=SCHEMA), default=StatusSugerido.Created, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class GruposTresModel(Base):
    """Modelo para Grupos_Tres."""
    __tablename__ = "Grupos_Tres"
    __table_args__ = {"schema": SCHEMA}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    grupo_tres = Column("Grupo_Tres", String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class GruposCuatroModel(Base):
    """Modelo para Grupos_Cuatro."""
    __tablename__ = "Grupos_Cuatro"
    __table_args__ = {"schema": SCHEMA}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    grupo_cuatro = Column("Grupo_Cuatro", String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class GruposCincoModel(Base):
    """Modelo para Grupos_Cinco."""
    __tablename__ = "Grupos_Cinco"
    __table_args__ = {"schema": SCHEMA}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    grupo_cinco = Column("Grupo_Cinco", String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
