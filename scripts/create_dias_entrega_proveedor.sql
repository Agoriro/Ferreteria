-- Script para crear la tabla dias_entrega_proveedor en PostgreSQL
-- Ejecutar este script en la base de datos Ferreteria, schema Pedidos

-- Eliminar la tabla si existe (CUIDADO: esto borra todos los datos)
DROP TABLE IF EXISTS "Pedidos".dias_entrega_proveedor CASCADE;

-- Crear tabla dias_entrega_proveedor en el schema Pedidos
CREATE TABLE "Pedidos".dias_entrega_proveedor (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empresa VARCHAR(100) NOT NULL,
    nit_proveedor VARCHAR(200) NOT NULL,
    dias_entrega INTEGER NOT NULL
);

-- Índice para búsqueda por empresa y NIT
CREATE INDEX idx_dias_entrega_empresa_nit
ON "Pedidos".dias_entrega_proveedor(empresa, nit_proveedor);

-- Índice único para garantizar que no haya duplicados
CREATE UNIQUE INDEX ux_dias_entrega_empresa_nit
ON "Pedidos".dias_entrega_proveedor(empresa, nit_proveedor);

-- Comentarios de la tabla
COMMENT ON TABLE "Pedidos".dias_entrega_proveedor IS 'Días de entrega configurados por proveedor y empresa';
COMMENT ON COLUMN "Pedidos".dias_entrega_proveedor.id IS 'Identificador único UUID';
COMMENT ON COLUMN "Pedidos".dias_entrega_proveedor.empresa IS 'Código o nombre de la empresa';
COMMENT ON COLUMN "Pedidos".dias_entrega_proveedor.nit_proveedor IS 'NIT o identificación del proveedor';
COMMENT ON COLUMN "Pedidos".dias_entrega_proveedor.dias_entrega IS 'Cantidad de días estimados de entrega';



