-- =====================================================
-- Script para crear tabla Vista_Tabla_Terceros en PostgreSQL
-- Basada en la vista de SQL Server
-- Schema: Pedidos
-- =====================================================

-- Crear extensión para búsquedas con LIKE (opcional)
-- Si no tienes permisos de superusuario, comenta esta línea
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Crear tabla Vista_Tabla_Terceros
CREATE TABLE IF NOT EXISTS "public"."Vista_Tabla_Terceros" (
    -- ID único para PostgreSQL
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Campos de la vista original
    "Fecha_Creacion" TIMESTAMP WITH TIME ZONE,
    "Autonumerico" INTEGER,
    "Tipo_de_Identificacion" VARCHAR(100),
    "Identificacion" VARCHAR(25) NOT NULL,
    "Digito_de_Verificacion" VARCHAR(1),
    "Ciudad_de_Identificacion" VARCHAR(255),
    "Codigo_Tercero" VARCHAR(15),
    "Primer_Nombre" VARCHAR(120),
    "Segundo_Nombre" VARCHAR(50),
    "Primer_Apellido" VARCHAR(50),
    "Segundo_Apellido" VARCHAR(50),
    "Nombre" VARCHAR(255),
    "Direccion" VARCHAR(255),
    "Email" VARCHAR(255),
    "Apellidos" VARCHAR(120),
    "Propiedades" VARCHAR(255),
    "Nota" VARCHAR(500),
    "Activo" SMALLINT DEFAULT 0,
    "Clasificacion_Uno" VARCHAR(255),
    "Clasificacion_Dos" VARCHAR(255),
    "Clasificacion_Tres" VARCHAR(255),
    "Plazo" INTEGER DEFAULT 0,
    "Tipo_de_Contribuyente" VARCHAR(255),
    "Cupo_de_Credito" NUMERIC(28, 6) DEFAULT 0,
    "Maneja_Cupo_de_Credito" SMALLINT DEFAULT 0,
    "Lista_de_Precios" VARCHAR(50),
    "Personalizado1" VARCHAR(500),
    "Personalizado2" VARCHAR(500),
    "Personalizado3" VARCHAR(500),
    "Personalizado4" VARCHAR(500),
    "Personalizado5" VARCHAR(500),
    "Personalizado6" VARCHAR(500),
    "Personalizado7" VARCHAR(500),
    "Personalizado8" VARCHAR(500),
    "Personalizado9" VARCHAR(500),
    "Personalizado10" VARCHAR(500),
    "Personalizado11" VARCHAR(500),
    "Personalizado12" VARCHAR(500),
    "Personalizado13" VARCHAR(500),
    "Personalizado14" VARCHAR(500),
    "Personalizado15" VARCHAR(500),
    "Zona_Uno" VARCHAR(255),
    "Zona_Dos" VARCHAR(255),
    "Vendedor" VARCHAR(255),
    "Nombre_Vendedor" VARCHAR(255),
    "IdTercero" INTEGER,
    "IdTipoIdentificacion" INTEGER,
    "DV" VARCHAR(1),
    "IdentificacionCiudad" INTEGER,
    "CodigoTercero" VARCHAR(15),
    "IdClasificacionUno" INTEGER,
    "IdClasificacionDos" INTEGER,
    "IdClasificacionTres" INTEGER,
    "IdPropiedadRetencion" INTEGER,
    "CupoCredito" NUMERIC(28, 6),
    "SenCupoCredito" SMALLINT,
    "ListPrecios" VARCHAR(50),
    "IdZonaUno" INTEGER,
    "IdZonaDos" INTEGER,
    "VersionCol" BYTEA,
    "NomZonaUno" VARCHAR(255),
    "nomZonaDos" VARCHAR(255),
    "Codigo_Actividad_Economica" VARCHAR(50),
    "Descripcion_Actividad_Economica" VARCHAR(255),
    "FormaDePago" VARCHAR(255),
    "FechaDeCreacion" TIMESTAMP WITH TIME ZONE,
    "Fecha_Aniversario" DATE,
    
    -- Auditoría
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- ÍNDICES
-- =====================================================

-- Índice único para ON CONFLICT (Tipo_de_Identificacion + Identificacion + Digito_de_Verificacion)
CREATE UNIQUE INDEX IF NOT EXISTS ux_terceros_tipo_ident_dv
ON "public"."Vista_Tabla_Terceros"(
    COALESCE("Tipo_de_Identificacion", ''), 
    "Identificacion", 
    COALESCE("Digito_de_Verificacion", '')
);

-- Índice para búsqueda por Propiedades
CREATE INDEX IF NOT EXISTS idx_terceros_propiedades
ON "public"."Vista_Tabla_Terceros"("Propiedades");

-- Índice para búsqueda por Propiedades con texto parcial (LIKE)
-- Requiere la extensión pg_trgm. Si falla, se omite.
DO $$
BEGIN
    CREATE INDEX IF NOT EXISTS idx_terceros_propiedades_trgm
    ON "public"."Vista_Tabla_Terceros" USING gin ("Propiedades" gin_trgm_ops);
EXCEPTION WHEN undefined_object THEN
    RAISE NOTICE 'Extension pg_trgm no disponible. Indice trgm no creado.';
END $$;

-- Índice para búsqueda por Identificacion
CREATE INDEX IF NOT EXISTS idx_terceros_identificacion
ON "public"."Vista_Tabla_Terceros"("Identificacion");

-- Índice para búsqueda por IdTercero
CREATE INDEX IF NOT EXISTS idx_terceros_idtercero
ON "public"."Vista_Tabla_Terceros"("IdTercero");

-- Índice para búsqueda por nombre completo
CREATE INDEX IF NOT EXISTS idx_terceros_nombres
ON "public"."Vista_Tabla_Terceros"("Primer_Nombre", "Primer_Apellido");

-- Índice para búsqueda por Nombre (campo concatenado)
CREATE INDEX IF NOT EXISTS idx_terceros_nombre
ON "public"."Vista_Tabla_Terceros"("Nombre");

-- Índice para búsqueda por email
CREATE INDEX IF NOT EXISTS idx_terceros_email
ON "public"."Vista_Tabla_Terceros"("Email");

-- Índice para filtrar por Activo
CREATE INDEX IF NOT EXISTS idx_terceros_activo
ON "public"."Vista_Tabla_Terceros"("Activo");

-- Índice para búsqueda por Codigo_Tercero
CREATE INDEX IF NOT EXISTS idx_terceros_codigo
ON "public"."Vista_Tabla_Terceros"("Codigo_Tercero");

-- =====================================================
-- COMENTARIOS
-- =====================================================

COMMENT ON TABLE "public"."Vista_Tabla_Terceros" 
    IS 'Tabla de terceros (clientes, proveedores, etc.) basada en Vista_Tabla_Terceros de SQL Server';

COMMENT ON COLUMN "public"."Vista_Tabla_Terceros".id 
    IS 'Identificador único UUID para PostgreSQL';

COMMENT ON COLUMN "public"."Vista_Tabla_Terceros"."Tipo_de_Identificacion" 
    IS 'Tipo de documento de identificación (CC, NIT, CE, etc.)';

COMMENT ON COLUMN "public"."Vista_Tabla_Terceros"."Identificacion" 
    IS 'Número de identificación del tercero';

COMMENT ON COLUMN "public"."Vista_Tabla_Terceros"."Digito_de_Verificacion" 
    IS 'Dígito de verificación (para NIT)';

COMMENT ON COLUMN "public"."Vista_Tabla_Terceros"."Propiedades" 
    IS 'Propiedades del tercero (Cliente, Proveedor, Empleado, etc.)';

COMMENT ON COLUMN "public"."Vista_Tabla_Terceros"."IdTercero" 
    IS 'ID original del tercero en SQL Server';

-- =====================================================
-- Mensaje de confirmación
-- =====================================================

DO $$
BEGIN
    RAISE NOTICE '=====================================================';
    RAISE NOTICE 'Tabla Vista_Tabla_Terceros creada exitosamente!';
    RAISE NOTICE 'Indice unico: Tipo_de_Identificacion + Identificacion + Digito_de_Verificacion';
    RAISE NOTICE 'Indice para busqueda por Propiedades creado';
    RAISE NOTICE '=====================================================';
END $$;
