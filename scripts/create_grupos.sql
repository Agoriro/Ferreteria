-- Script para crear las tablas de Grupos (Tres, Cuatro, Cinco)
-- Ejecutar en PostgreSQL/Supabase

-- Tabla Grupos_Tres
CREATE TABLE IF NOT EXISTS public."Grupos_Tres" (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    "Grupo_Tres" VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT Grupos_Tres_pkey PRIMARY KEY (id),
    CONSTRAINT Grupos_Tres_Grupo_Tres_key UNIQUE ("Grupo_Tres")
);

CREATE INDEX IF NOT EXISTS idx_grupos_tres_nombre 
ON public."Grupos_Tres" USING btree ("Grupo_Tres");

-- Tabla Grupos_Cuatro
CREATE TABLE IF NOT EXISTS public."Grupos_Cuatro" (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    "Grupo_Cuatro" VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT Grupos_Cuatro_pkey PRIMARY KEY (id),
    CONSTRAINT Grupos_Cuatro_Grupo_Cuatro_key UNIQUE ("Grupo_Cuatro")
);

CREATE INDEX IF NOT EXISTS idx_grupos_cuatro_nombre 
ON public."Grupos_Cuatro" USING btree ("Grupo_Cuatro");

-- Tabla Grupos_Cinco
CREATE TABLE IF NOT EXISTS public."Grupos_Cinco" (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    "Grupo_Cinco" VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT Grupos_Cinco_pkey PRIMARY KEY (id),
    CONSTRAINT Grupos_Cinco_Grupo_Cinco_key UNIQUE ("Grupo_Cinco")
);

CREATE INDEX IF NOT EXISTS idx_grupos_cinco_nombre 
ON public."Grupos_Cinco" USING btree ("Grupo_Cinco");

-- Mensaje de confirmación
DO $$
BEGIN
    RAISE NOTICE 'Tablas Grupos_Tres, Grupos_Cuatro y Grupos_Cinco creadas exitosamente';
END $$;
