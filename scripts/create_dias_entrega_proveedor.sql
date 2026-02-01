-- Script para crear la tabla dias_entrega_proveedor en PostgreSQL
-- Ejecutar este script en la base de datos Ferreteria, schema Pedidos

-- Eliminar la tabla si existe (CUIDADO: esto borra todos los datos)
DROP TABLE IF EXISTS "public".dias_entrega_proveedor CASCADE;

-- Crear tabla dias_entrega_proveedor en el schema Pedidos
CREATE TABLE "public".dias_entrega_proveedor (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empresa VARCHAR(100) NOT NULL,
    nit_proveedor VARCHAR(200) NOT NULL,
    codigo_producto VARCHAR(100) NOT NULL,
    dias_entrega INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice para búsqueda por empresa
CREATE INDEX idx_dias_entrega_empresa
ON "public".dias_entrega_proveedor(empresa);

-- Índice para búsqueda por empresa y NIT
CREATE INDEX idx_dias_entrega_empresa_nit
ON "public".dias_entrega_proveedor(empresa, nit_proveedor);

-- Índice para búsqueda por empresa y producto
CREATE INDEX idx_dias_entrega_empresa_producto
ON "public".dias_entrega_proveedor(empresa, codigo_producto);

-- Índice único para garantizar que no haya duplicados (empresa + proveedor + producto)
CREATE UNIQUE INDEX ux_dias_entrega_empresa_nit_producto
ON "public".dias_entrega_proveedor(empresa, nit_proveedor, codigo_producto);

-- Comentarios de la tabla
COMMENT ON TABLE "public".dias_entrega_proveedor IS 'Días de entrega configurados por proveedor, producto y empresa';
COMMENT ON COLUMN "public".dias_entrega_proveedor.id IS 'Identificador único UUID';
COMMENT ON COLUMN "public".dias_entrega_proveedor.empresa IS 'Código o nombre de la empresa';
COMMENT ON COLUMN "public".dias_entrega_proveedor.nit_proveedor IS 'NIT o identificación del proveedor';
COMMENT ON COLUMN "public".dias_entrega_proveedor.codigo_producto IS 'Código del producto';
COMMENT ON COLUMN "public".dias_entrega_proveedor.dias_entrega IS 'Cantidad de días estimados de entrega';
COMMENT ON COLUMN "public".dias_entrega_proveedor.created_at IS 'Fecha de creación del registro';
COMMENT ON COLUMN "public".dias_entrega_proveedor.updated_at IS 'Fecha de última actualización';

-- Script para agregar columna si la tabla ya existe (alternativa sin DROP)
-- ALTER TABLE "public".dias_entrega_proveedor ADD COLUMN IF NOT EXISTS codigo_producto VARCHAR(100);
-- ALTER TABLE "public".dias_entrega_proveedor ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
-- ALTER TABLE "public".dias_entrega_proveedor ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
