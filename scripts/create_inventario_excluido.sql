-- Script para crear la tabla inventario_excluido en PostgreSQL
-- Ejecutar este script en la base de datos Ferreteria, schema Pedidos

-- Eliminar la tabla si existe (CUIDADO: esto borra todos los datos)
DROP TABLE IF EXISTS "public".inventario_excluido CASCADE;

-- Crear tabla inventario_excluido en el schema Pedidos
-- Usa gen_random_uuid() que es nativa de PostgreSQL 13+
CREATE TABLE "public".inventario_excluido (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo_producto VARCHAR(100) NOT NULL,
    status BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índice para búsqueda por código de producto
CREATE INDEX idx_inventario_excluido_codigo_producto 
ON "public".inventario_excluido(codigo_producto);

-- Índice para filtrar por status
CREATE INDEX idx_inventario_excluido_status 
ON "public".inventario_excluido(status);

-- Función para actualizar automáticamente updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para actualizar updated_at automáticamente
DROP TRIGGER IF EXISTS update_inventario_excluido_updated_at ON "public".inventario_excluido;
CREATE TRIGGER update_inventario_excluido_updated_at
    BEFORE UPDATE ON "public".inventario_excluido
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Comentarios de la tabla
COMMENT ON TABLE "public".inventario_excluido IS 'Tabla para gestionar productos excluidos del inventario';
COMMENT ON COLUMN "public".inventario_excluido.id IS 'Identificador único UUID';
COMMENT ON COLUMN "public".inventario_excluido.codigo_producto IS 'Código del producto excluido';
COMMENT ON COLUMN "public".inventario_excluido.status IS 'Estado del registro (true=activo, false=inactivo)';
COMMENT ON COLUMN "public".inventario_excluido.created_at IS 'Fecha de creación del registro';
COMMENT ON COLUMN "public".inventario_excluido.updated_at IS 'Fecha de última actualización';

