-- =====================================================
-- Script de Datos Semilla para Sistema de Permisos
-- Proyecto: Ferreteria API
-- =====================================================

-- =====================================================
-- PASO 1: Insertar los Roles (ADMIN, USER, MANAGER)
-- =====================================================

INSERT INTO "public".roles (nombre_rol, descripcion)
VALUES 
    ('ADMIN', 'Administrador del sistema con acceso completo'),
    ('USER', 'Usuario estándar con acceso limitado'),
    ('MANAGER', 'Gerente con acceso a requisiciones')
ON CONFLICT (nombre_rol) DO UPDATE SET 
    descripcion = EXCLUDED.descripcion;

-- =====================================================
-- PASO 2: Insertar los Formularios
-- =====================================================

INSERT INTO "public".formularios (nombre_formulario, descripcion, ruta)
VALUES 
    ('Administración de usuarios', 'Gestión de usuarios del sistema', '/admin/usuarios'),
    ('Inventario Excluido', 'Productos excluidos del inventario', '/inventario-excluido'),
    ('Días Entrega Proveedor', 'Configuración de días de entrega por proveedor', '/dias-entrega-proveedor'),
    ('Sugerido de compras', 'Sugerencias de compras basadas en inventario', '/sugerido-compras'),
    ('Requisición de compras', 'Requisiciones de compra a proveedores', '/requisicion-compras'),
    ('Exportar Requisiciones', 'Exportación de requisiciones', '/exportar-requisiciones'),
    ('Reportes', 'Reportes y estadísticas del sistema', '/reportes')
ON CONFLICT (nombre_formulario) DO UPDATE SET
    descripcion = EXCLUDED.descripcion,
    ruta = EXCLUDED.ruta;

-- =====================================================
-- PASO 3: Limpiar Permisos Existentes (opcional)
-- =====================================================
-- DELETE FROM "public".detalle_permisos;

-- =====================================================
-- PASO 4: Insertar Permisos para ADMIN (todos los formularios)
-- =====================================================

INSERT INTO "public".detalle_permisos (id_rol, id_formulario, puede_leer, puede_crear, puede_editar, puede_eliminar)
SELECT r.id_rol, f.id_formulario, true, true, true, true
FROM "public".roles r
CROSS JOIN "public".formularios f
WHERE r.nombre_rol = 'ADMIN'
ON CONFLICT DO NOTHING;

-- =====================================================
-- PASO 5: Insertar Permisos para USER
-- Formularios: Sugerido de compras, Requisición de compras, 
--              Exportar Requisiciones, Reportes
-- =====================================================

INSERT INTO "public".detalle_permisos (id_rol, id_formulario, puede_leer, puede_crear, puede_editar, puede_eliminar)
SELECT r.id_rol, f.id_formulario, true, true, true, false
FROM "public".roles r
CROSS JOIN "public".formularios f
WHERE r.nombre_rol = 'USER'
  AND f.nombre_formulario IN (
      'Sugerido de compras',
      'Requisición de compras',
      'Exportar Requisiciones',
      'Reportes'
  )
ON CONFLICT DO NOTHING;

-- =====================================================
-- PASO 6: Insertar Permisos para MANAGER
-- Formularios: Requisición de compras
-- =====================================================

INSERT INTO "public".detalle_permisos (id_rol, id_formulario, puede_leer, puede_crear, puede_editar, puede_eliminar)
SELECT r.id_rol, f.id_formulario, true, true, false, false
FROM "public".roles r
CROSS JOIN "public".formularios f
WHERE r.nombre_rol = 'MANAGER'
  AND f.nombre_formulario = 'Requisición de compras'
ON CONFLICT DO NOTHING;

-- =====================================================
-- Verificación de datos insertados
-- =====================================================
DO $$
DECLARE
    v_roles INTEGER;
    v_formularios INTEGER;
    v_permisos INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_roles FROM "public".roles;
    SELECT COUNT(*) INTO v_formularios FROM "public".formularios;
    SELECT COUNT(*) INTO v_permisos FROM "public".detalle_permisos;
    
    RAISE NOTICE '=====================================================';
    RAISE NOTICE 'Datos Semilla Insertados:';
    RAISE NOTICE 'Roles: %', v_roles;
    RAISE NOTICE 'Formularios: %', v_formularios;
    RAISE NOTICE 'Permisos: %', v_permisos;
    RAISE NOTICE '=====================================================';
END $$;

-- =====================================================
-- Consulta de verificación (ejecutar manualmente)
-- =====================================================
-- SELECT 
--     r.nombre_rol,
--     f.nombre_formulario,
--     dp.puede_leer,
--     dp.puede_crear,
--     dp.puede_editar,
--     dp.puede_eliminar
-- FROM "public".detalle_permisos dp
-- JOIN "public".roles r ON dp.id_rol = r.id_rol
-- JOIN "public".formularios f ON dp.id_formulario = f.id_formulario
-- ORDER BY r.nombre_rol, f.nombre_formulario;
