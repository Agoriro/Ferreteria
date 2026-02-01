-- =====================================================
-- Script para crear tabla Sugerido de Compras
-- Schema: Pedidos
-- =====================================================

-- Crear tipo ENUM para status
DO $$ BEGIN
    CREATE TYPE "public".status_sugerido AS ENUM ('Created', 'Requested', 'Processed');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- =====================================================
-- TABLA: sugerido_compras
-- =====================================================
CREATE TABLE IF NOT EXISTS "public".sugerido_compras (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empresa VARCHAR(100) NOT NULL,
    fecha DATE,
    num_doc VARCHAR(100),
    proveedor VARCHAR(255),
    grupo3 VARCHAR(255),
    grupo4 VARCHAR(255),
    grupo5 VARCHAR(255),
    cod_prod VARCHAR(100) NOT NULL,
    descripcion VARCHAR(500),
    unidad_medida VARCHAR(50),
    exist NUMERIC(28, 6) DEFAULT 0,
    exist_mc NUMERIC(28, 6) DEFAULT 0,
    cantidad_ventas_anterior NUMERIC(28, 6) DEFAULT 0,
    cantidad_ventas_actual NUMERIC(28, 6) DEFAULT 0,
    sugerido_compras NUMERIC(28, 6) DEFAULT 0,
    cantidad_a_pedir NUMERIC(28, 6) DEFAULT 0,
    proveedor1 VARCHAR(255),
    proveedor2 VARCHAR(255),
    proveedor3 VARCHAR(255),
    proveedor4 VARCHAR(255),
    compras_en_el_periodo NUMERIC(28, 6) DEFAULT 0,
    total_entradas_en_el_periodo NUMERIC(28, 6) DEFAULT 0,
    ultima_fecha_compra DATE,
    ventas_en_el_periodo NUMERIC(28, 6) DEFAULT 0,
    total_salidas_en_el_periodo NUMERIC(28, 6) DEFAULT 0,
    ultima_fecha_venta DATE,
    saldo_actual NUMERIC(28, 6) DEFAULT 0,
    val_unit NUMERIC(28, 6) DEFAULT 0,
    dcto NUMERIC(28, 6) DEFAULT 0,
    val_neto NUMERIC(28, 6) DEFAULT 0,
    precio1 NUMERIC(28, 6) DEFAULT 0,
    util_1 NUMERIC(28, 6) DEFAULT 0,
    precio2 NUMERIC(28, 6) DEFAULT 0,
    util_2 NUMERIC(28, 6) DEFAULT 0,
    status "public".status_sugerido DEFAULT 'Created',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indices
CREATE INDEX IF NOT EXISTS idx_sugerido_compras_empresa ON "public".sugerido_compras(empresa);
CREATE INDEX IF NOT EXISTS idx_sugerido_compras_cod_prod ON "public".sugerido_compras(cod_prod);
CREATE INDEX IF NOT EXISTS idx_sugerido_compras_status ON "public".sugerido_compras(status);
CREATE INDEX IF NOT EXISTS idx_sugerido_compras_fecha ON "public".sugerido_compras(fecha);

-- =====================================================
-- Mensaje de confirmacion
-- =====================================================
DO $$
BEGIN
    RAISE NOTICE 'Tabla sugerido_compras creada correctamente!';
END $$;

