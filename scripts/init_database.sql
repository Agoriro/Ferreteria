-- =====================================================
-- Script de inicializacion de base de datos
-- Proyecto: Ferreteria API
-- =====================================================

-- En Supabase usamos el schema "public" que ya existe por defecto
-- No es necesario crear el schema

-- =====================================================
-- TABLA: roles
-- =====================================================
CREATE TABLE IF NOT EXISTS "public".roles (
    id_rol SERIAL PRIMARY KEY,
    nombre_rol VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- =====================================================
-- TABLA: formularios
-- =====================================================
CREATE TABLE IF NOT EXISTS "public".formularios (
    id_formulario SERIAL PRIMARY KEY,
    nombre_formulario VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    ruta VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABLA: detalle_permisos
-- =====================================================
CREATE TABLE IF NOT EXISTS "public".detalle_permisos (
    id_permiso SERIAL PRIMARY KEY,
    id_rol INTEGER NOT NULL REFERENCES "public".roles(id_rol) ON DELETE CASCADE,
    id_formulario INTEGER NOT NULL REFERENCES "public".formularios(id_formulario) ON DELETE CASCADE,
    puede_leer BOOLEAN DEFAULT TRUE,
    puede_crear BOOLEAN DEFAULT FALSE,
    puede_editar BOOLEAN DEFAULT FALSE,
    puede_eliminar BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABLA: usuarios
-- =====================================================
CREATE TABLE IF NOT EXISTS "public".usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    id_proveedor INTEGER,
    estado BOOLEAN DEFAULT TRUE,
    rol_id INTEGER NOT NULL REFERENCES "public".roles(id_rol),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Indices para usuarios
CREATE INDEX IF NOT EXISTS idx_usuarios_username ON "public".usuarios(username);
CREATE INDEX IF NOT EXISTS idx_usuarios_estado ON "public".usuarios(estado);

-- =====================================================
-- TABLA: refresh_tokens
-- =====================================================
CREATE TABLE IF NOT EXISTS "public".refresh_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "public".usuarios(id) ON DELETE CASCADE,
    token VARCHAR(500) UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    revoked BOOLEAN DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_refresh_tokens_token ON "public".refresh_tokens(token);

-- =====================================================
-- TABLA: inventario_excluido
-- =====================================================
CREATE TABLE IF NOT EXISTS "public".inventario_excluido (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo_producto VARCHAR(100) NOT NULL,
    empresa VARCHAR(100) NOT NULL,
    status BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_inventario_excluido_codigo ON "public".inventario_excluido(codigo_producto);
CREATE INDEX IF NOT EXISTS idx_inventario_excluido_empresa ON "public".inventario_excluido(empresa);
CREATE INDEX IF NOT EXISTS idx_inventario_excluido_status ON "public".inventario_excluido(status);

-- =====================================================
-- TABLA: dias_entrega_proveedor
-- =====================================================
CREATE TABLE IF NOT EXISTS "public".dias_entrega_proveedor (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empresa VARCHAR(100) NOT NULL,
    nit_proveedor VARCHAR(200) NOT NULL,
    dias_entrega INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_dias_entrega_empresa ON "public".dias_entrega_proveedor(empresa);
CREATE INDEX IF NOT EXISTS idx_dias_entrega_nit ON "public".dias_entrega_proveedor(nit_proveedor);

-- =====================================================
-- DATOS INICIALES
-- =====================================================

-- Rol administrador
INSERT INTO "public".roles (nombre_rol, descripcion)
VALUES ('admin', 'Administrador del sistema con acceso completo')
ON CONFLICT (nombre_rol) DO NOTHING;

-- Rol usuario
INSERT INTO "public".roles (nombre_rol, descripcion)
VALUES ('usuario', 'Usuario estandar con acceso limitado')
ON CONFLICT (nombre_rol) DO NOTHING;

-- Usuario administrador por defecto
-- Password: admin123 (hash bcrypt)
INSERT INTO "public".usuarios (username, password, nombres, apellidos, rol_id, estado)
SELECT 'admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYn1qVGVXYGK', 'Administrador', 'Sistema', r.id_rol, true
FROM "public".roles r
WHERE r.nombre_rol = 'admin'
ON CONFLICT (username) DO NOTHING;

-- =====================================================
-- Mensaje de confirmacion
-- =====================================================
DO $$
BEGIN
    RAISE NOTICE '=====================================================';
    RAISE NOTICE 'Base de datos inicializada correctamente!';
    RAISE NOTICE 'Usuario: admin';
    RAISE NOTICE 'Password: admin123';
    RAISE NOTICE '=====================================================';
END $$;

