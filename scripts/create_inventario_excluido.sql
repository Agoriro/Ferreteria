-- Script para crear la tabla inventario_excluido en PostgreSQL
-- Ejecutar este script en la base de datos PostgreSQL

-- Extensión para UUID (si no está habilitada)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Crear tabla inventario_excluido
CREATE TABLE IF NOT EXISTS inventario_excluido (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    codigo_producto VARCHAR(100) NOT NULL,
    status BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índice para búsqueda por código de producto
CREATE INDEX IF NOT EXISTS idx_inventario_excluido_codigo_producto 
ON inventario_excluido(codigo_producto);

-- Índice para filtrar por status
CREATE INDEX IF NOT EXISTS idx_inventario_excluido_status 
ON inventario_excluido(status);

-- Función para actualizar automáticamente updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para actualizar updated_at automáticamente
DROP TRIGGER IF EXISTS update_inventario_excluido_updated_at ON inventario_excluido;
CREATE TRIGGER update_inventario_excluido_updated_at
    BEFORE UPDATE ON inventario_excluido
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Comentarios de la tabla
COMMENT ON TABLE inventario_excluido IS 'Tabla para gestionar productos excluidos del inventario';
COMMENT ON COLUMN inventario_excluido.id IS 'Identificador único UUID';
COMMENT ON COLUMN inventario_excluido.codigo_producto IS 'Código del producto excluido';
COMMENT ON COLUMN inventario_excluido.status IS 'Estado del registro (true=activo, false=inactivo)';
COMMENT ON COLUMN inventario_excluido.created_at IS 'Fecha de creación del registro';
COMMENT ON COLUMN inventario_excluido.updated_at IS 'Fecha de última actualización';

