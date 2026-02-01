-- =====================================================
-- Script ALTER para modificar tabla dias_entrega_proveedor
-- Agrega: codigo_producto, created_at, updated_at
-- =====================================================

-- 1. Agregar columna codigo_producto (temporalmente nullable)
ALTER TABLE "public".dias_entrega_proveedor
ADD COLUMN IF NOT EXISTS codigo_producto VARCHAR(100);

-- 2. Agregar columnas de auditoría
ALTER TABLE "public".dias_entrega_proveedor
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

ALTER TABLE "public".dias_entrega_proveedor
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- 3. Actualizar registros existentes con valor temporal para codigo_producto
-- (Puedes cambiar 'PENDIENTE' por otro valor o actualizar manualmente después)
UPDATE "public".dias_entrega_proveedor
SET codigo_producto = 'TODOS'
WHERE codigo_producto IS NULL;

-- 4. Hacer codigo_producto NOT NULL después de asignar valores
ALTER TABLE "public".dias_entrega_proveedor
ALTER COLUMN codigo_producto SET NOT NULL;

-- 5. Eliminar el índice único anterior (empresa + nit_proveedor)
DROP INDEX IF EXISTS "public".ux_dias_entrega_empresa_nit;

-- 6. Crear nuevo índice único (empresa + nit_proveedor + codigo_producto)
CREATE UNIQUE INDEX IF NOT EXISTS ux_dias_entrega_empresa_nit_producto
ON "public".dias_entrega_proveedor(empresa, nit_proveedor, codigo_producto);

-- 7. Crear índice para búsqueda por empresa y producto
CREATE INDEX IF NOT EXISTS idx_dias_entrega_empresa_producto
ON "public".dias_entrega_proveedor(empresa, codigo_producto);

-- 8. Crear índice para búsqueda solo por codigo_producto
CREATE INDEX IF NOT EXISTS idx_dias_entrega_producto
ON "public".dias_entrega_proveedor(codigo_producto);

-- 9. Actualizar comentarios
COMMENT ON COLUMN "public".dias_entrega_proveedor.codigo_producto
    IS 'Código del producto';

COMMENT ON COLUMN "public".dias_entrega_proveedor.created_at
    IS 'Fecha de creación del registro';

COMMENT ON COLUMN "public".dias_entrega_proveedor.updated_at
    IS 'Fecha de última actualización';

-- =====================================================
-- Verificar estructura final
-- =====================================================
DO $$
BEGIN
    RAISE NOTICE '=====================================================';
    RAISE NOTICE 'Tabla dias_entrega_proveedor modificada exitosamente!';
    RAISE NOTICE 'Nuevas columnas: codigo_producto, created_at, updated_at';
    RAISE NOTICE 'Nuevo indice unico: empresa + nit_proveedor + codigo_producto';
    RAISE NOTICE '=====================================================';
    RAISE NOTICE 'IMPORTANTE: Los registros existentes tienen codigo_producto = TODOS';
    RAISE NOTICE 'Actualiza manualmente los registros si es necesario.';
    RAISE NOTICE '=====================================================';
END $$;

