# Documentación del Endpoint de Permisos

## Descripción General

Este endpoint permite obtener la lista de formularios a los que tiene acceso un usuario según su rol. Es útil para que el frontend determine qué opciones del menú mostrar a cada usuario.

---

## Endpoints Disponibles

### 1. Obtener Formularios por Rol

**Endpoint:**
```
GET /api/v1/permisos/formularios/{nombre_rol}
```

**Descripción:**  
Retorna la lista de formularios a los que tiene acceso un rol específico.

**Parámetros de Ruta:**
| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `nombre_rol` | string | Sí | Nombre del rol (`ADMIN`, `USER`, `MANAGER`) |

**Headers Requeridos:**
| Header | Valor | Descripción |
|--------|-------|-------------|
| `Authorization` | `Bearer {token}` | Token JWT de autenticación |

**Ejemplo de Request (cURL):**
```bash
curl -X GET "http://localhost:8000/api/v1/permisos/formularios/ADMIN" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

**Ejemplo de Request (JavaScript/Fetch):**
```javascript
const token = localStorage.getItem('access_token');

const response = await fetch('http://localhost:8000/api/v1/permisos/formularios/ADMIN', {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    }
});

const data = await response.json();
console.log(data);
```

**Ejemplo de Request (Axios):**
```javascript
import axios from 'axios';

const token = localStorage.getItem('access_token');

const response = await axios.get('/api/v1/permisos/formularios/ADMIN', {
    headers: {
        'Authorization': `Bearer ${token}`
    }
});

console.log(response.data);
```

**Respuesta Exitosa (200 OK):**
```json
{
    "rol": "ADMIN",
    "formularios": [
        {
            "id_formulario": 1,
            "nombre_formulario": "Administración de usuarios",
            "descripcion": "Gestión de usuarios del sistema",
            "ruta": "/admin/usuarios",
            "puede_leer": true,
            "puede_crear": true,
            "puede_editar": true,
            "puede_eliminar": true
        },
        {
            "id_formulario": 2,
            "nombre_formulario": "Inventario Excluido",
            "descripcion": "Productos excluidos del inventario",
            "ruta": "/inventario-excluido",
            "puede_leer": true,
            "puede_crear": true,
            "puede_editar": true,
            "puede_eliminar": true
        },
        {
            "id_formulario": 3,
            "nombre_formulario": "Días Entrega Proveedor",
            "descripcion": "Configuración de días de entrega por proveedor",
            "ruta": "/dias-entrega-proveedor",
            "puede_leer": true,
            "puede_crear": true,
            "puede_editar": true,
            "puede_eliminar": true
        },
        {
            "id_formulario": 4,
            "nombre_formulario": "Sugerido de compras",
            "descripcion": "Sugerencias de compras basadas en inventario",
            "ruta": "/sugerido-compras",
            "puede_leer": true,
            "puede_crear": true,
            "puede_editar": true,
            "puede_eliminar": true
        },
        {
            "id_formulario": 5,
            "nombre_formulario": "Requisición de compras",
            "descripcion": "Requisiciones de compra a proveedores",
            "ruta": "/requisicion-compras",
            "puede_leer": true,
            "puede_crear": true,
            "puede_editar": true,
            "puede_eliminar": true
        },
        {
            "id_formulario": 6,
            "nombre_formulario": "Exportar Requisiciones",
            "descripcion": "Exportación de requisiciones",
            "ruta": "/exportar-requisiciones",
            "puede_leer": true,
            "puede_crear": true,
            "puede_editar": true,
            "puede_eliminar": true
        },
        {
            "id_formulario": 7,
            "nombre_formulario": "Reportes",
            "descripcion": "Reportes y estadísticas del sistema",
            "ruta": "/reportes",
            "puede_leer": true,
            "puede_crear": true,
            "puede_editar": true,
            "puede_eliminar": true
        }
    ]
}
```

**Respuesta para USER (4 formularios):**
```json
{
    "rol": "USER",
    "formularios": [
        {
            "id_formulario": 4,
            "nombre_formulario": "Sugerido de compras",
            "descripcion": "Sugerencias de compras basadas en inventario",
            "ruta": "/sugerido-compras",
            "puede_leer": true,
            "puede_crear": true,
            "puede_editar": true,
            "puede_eliminar": false
        },
        {
            "id_formulario": 5,
            "nombre_formulario": "Requisición de compras",
            "descripcion": "Requisiciones de compra a proveedores",
            "ruta": "/requisicion-compras",
            "puede_leer": true,
            "puede_crear": true,
            "puede_editar": true,
            "puede_eliminar": false
        },
        {
            "id_formulario": 6,
            "nombre_formulario": "Exportar Requisiciones",
            "descripcion": "Exportación de requisiciones",
            "ruta": "/exportar-requisiciones",
            "puede_leer": true,
            "puede_crear": true,
            "puede_editar": true,
            "puede_eliminar": false
        },
        {
            "id_formulario": 7,
            "nombre_formulario": "Reportes",
            "descripcion": "Reportes y estadísticas del sistema",
            "ruta": "/reportes",
            "puede_leer": true,
            "puede_crear": true,
            "puede_editar": true,
            "puede_eliminar": false
        }
    ]
}
```

**Respuesta para MANAGER (1 formulario):**
```json
{
    "rol": "MANAGER",
    "formularios": [
        {
            "id_formulario": 5,
            "nombre_formulario": "Requisición de compras",
            "descripcion": "Requisiciones de compra a proveedores",
            "ruta": "/requisicion-compras",
            "puede_leer": true,
            "puede_crear": true,
            "puede_editar": false,
            "puede_eliminar": false
        }
    ]
}
```

**Errores Posibles:**
| Código | Descripción |
|--------|-------------|
| 401 | Token no válido o expirado |
| 403 | Usuario inactivo |

---

### 2. Verificar Acceso a Formulario Específico

**Endpoint:**
```
GET /api/v1/permisos/verificar/{nombre_rol}/{nombre_formulario}
```

**Descripción:**  
Verifica si un rol tiene acceso a un formulario específico.

**Parámetros de Ruta:**
| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `nombre_rol` | string | Sí | Nombre del rol |
| `nombre_formulario` | string | Sí | Nombre exacto del formulario |

**Ejemplo de Request:**
```javascript
const response = await fetch(
    'http://localhost:8000/api/v1/permisos/verificar/USER/Sugerido de compras',
    {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    }
);
```

**Respuesta Exitosa (tiene acceso):**
```json
{
    "tiene_acceso": true,
    "permisos": {
        "puede_leer": true,
        "puede_crear": true,
        "puede_editar": true,
        "puede_eliminar": false
    }
}
```

**Respuesta cuando NO tiene acceso:**
```json
{
    "tiene_acceso": false,
    "permisos": null
}
```

---

## Integración con Frontend

### Ejemplo de Uso en React

```jsx
import { useEffect, useState } from 'react';
import axios from 'axios';

function usePermisos(rol) {
    const [formularios, setFormularios] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchPermisos = async () => {
            try {
                const token = localStorage.getItem('access_token');
                const response = await axios.get(
                    `/api/v1/permisos/formularios/${rol}`,
                    {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    }
                );
                setFormularios(response.data.formularios);
            } catch (error) {
                console.error('Error fetching permisos:', error);
            } finally {
                setLoading(false);
            }
        };

        if (rol) {
            fetchPermisos();
        }
    }, [rol]);

    return { formularios, loading };
}

// Uso en componente de menú
function MenuLateral({ userRole }) {
    const { formularios, loading } = usePermisos(userRole);

    if (loading) return <div>Cargando menú...</div>;

    return (
        <nav>
            {formularios.map((form) => (
                <a key={form.id_formulario} href={form.ruta}>
                    {form.nombre_formulario}
                </a>
            ))}
        </nav>
    );
}
```

### Ejemplo de Guardia de Ruta (React Router)

```jsx
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from './AuthContext';
import { usePermisos } from './usePermisos';

function ProtectedRoute({ children, requiredForm }) {
    const { user } = useAuth();
    const { formularios } = usePermisos(user?.rol?.nombre_rol);
    const location = useLocation();

    // Verificar si el formulario está en la lista de permitidos
    const hasAccess = formularios.some(
        (f) => f.nombre_formulario === requiredForm
    );

    if (!hasAccess) {
        return <Navigate to="/no-autorizado" state={{ from: location }} />;
    }

    return children;
}

// Uso:
<Route 
    path="/admin/usuarios" 
    element={
        <ProtectedRoute requiredForm="Administración de usuarios">
            <AdminUsuarios />
        </ProtectedRoute>
    } 
/>
```

---

## Matriz de Permisos de Referencia

| Formulario | ADMIN | USER | MANAGER |
|------------|:-----:|:----:|:-------:|
| Administración de usuarios | ✅ | ❌ | ❌ |
| Inventario Excluido | ✅ | ❌ | ❌ |
| Días Entrega Proveedor | ✅ | ❌ | ❌ |
| Sugerido de compras | ✅ | ✅ | ❌ |
| Requisición de compras | ✅ | ✅ | ✅ |
| Exportar Requisiciones | ✅ | ✅ | ❌ |
| Reportes | ✅ | ✅ | ❌ |

---

## Notas Importantes

1. **Autenticación Requerida**: Todos los endpoints requieren un token JWT válido en el header `Authorization`.

2. **Case-Insensitive**: El nombre del rol no es sensible a mayúsculas/minúsculas (se convierte a mayúsculas internamente).

3. **Rol No Existente**: Si se consulta un rol que no existe, se retorna una lista vacía de formularios.

4. **Caché Recomendado**: Se recomienda cachear los permisos en el frontend después del login para evitar llamadas repetidas.
