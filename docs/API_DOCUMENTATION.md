# 📚 Documentación API Ferretería

Documentación técnica para el equipo de Frontend.

---

## 📋 Información General

| Propiedad | Valor |
|-----------|-------|
| **Base URL** | `http://localhost:8000/api/v1` |
| **Versión** | 1.0.0 |
| **Formato** | JSON |
| **Autenticación** | Bearer Token (JWT) |

### URLs de Documentación Interactiva

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🔐 Autenticación

La API utiliza **JWT (JSON Web Tokens)** para la autenticación.

### Flujo de Autenticación

```
┌─────────────┐      POST /auth/login       ┌─────────────┐
│   Frontend  │ ─────────────────────────▶  │   Backend   │
│             │  username + password        │             │
│             │ ◀─────────────────────────  │             │
│             │  access_token +             │             │
│             │  refresh_token              │             │
└─────────────┘                             └─────────────┘

┌─────────────┐   GET /users (protected)    ┌─────────────┐
│   Frontend  │ ─────────────────────────▶  │   Backend   │
│             │  Authorization: Bearer xxx  │             │
│             │ ◀─────────────────────────  │             │
│             │  Response data              │             │
└─────────────┘                             └─────────────┘
```

### Tokens

| Token | Duración | Uso |
|-------|----------|-----|
| `access_token` | 30 minutos | Acceso a endpoints protegidos |
| `refresh_token` | 7 días | Renovar access_token sin re-login |

### Uso del Token

Incluir en el header de todas las peticiones protegidas:

```http
Authorization: Bearer <access_token>
```

---

## 🔑 Endpoints de Autenticación

### POST `/api/v1/auth/login`

Inicia sesión y obtiene tokens de acceso.

#### Request

**Content-Type:** `application/x-www-form-urlencoded`

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `username` | string | ✅ | Nombre de usuario |
| `password` | string | ✅ | Contraseña |

#### Ejemplo Request (JavaScript/Fetch)

```javascript
const formData = new URLSearchParams();
formData.append('username', 'admin');
formData.append('password', 'admin123');

const response = await fetch('http://localhost:8000/api/v1/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: formData
});

const data = await response.json();
// Guardar tokens
localStorage.setItem('access_token', data.access_token);
localStorage.setItem('refresh_token', data.refresh_token);
```

#### Ejemplo Request (Axios)

```javascript
const response = await axios.post('http://localhost:8000/api/v1/auth/login', 
  new URLSearchParams({
    username: 'admin',
    password: 'admin123'
  }), {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  }
);
```

#### Response 200 OK

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Errores

| Código | Descripción |
|--------|-------------|
| 401 | Credenciales incorrectas |
| 403 | Usuario inactivo |
| 422 | Error de validación |

---

### POST `/api/v1/auth/refresh-token`

Renueva el access_token usando el refresh_token.

#### Request

**Content-Type:** `application/json`

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Ejemplo Request

```javascript
const response = await fetch('http://localhost:8000/api/v1/auth/refresh-token', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    refresh_token: localStorage.getItem('refresh_token')
  })
});

const data = await response.json();
localStorage.setItem('access_token', data.access_token);
```

#### Response 200 OK

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 👤 Endpoints de Usuarios

> ⚠️ **Todos estos endpoints requieren autenticación**

### GET `/api/v1/users/me`

Obtiene información del usuario autenticado.

#### Ejemplo Request

```javascript
const response = await fetch('http://localhost:8000/api/v1/users/me', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});
```

#### Response 200 OK

```json
{
  "id": 1,
  "username": "admin",
  "nombres": "Admin",
  "apellidos": "Sistema",
  "id_proveedor": null,
  "estado": true,
  "rol_id": 1,
  "created_at": "2024-12-10T10:30:00Z",
  "updated_at": null
}
```

---

### GET `/api/v1/users`

Lista todos los usuarios.

#### Query Parameters

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `skip` | int | 0 | Registros a saltar (paginación) |
| `limit` | int | 100 | Máximo de registros |
| `include_inactive` | bool | false | Incluir usuarios inactivos |

#### Ejemplo Request

```javascript
const response = await fetch('http://localhost:8000/api/v1/users?skip=0&limit=10&include_inactive=false', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});
```

#### Response 200 OK

```json
[
  {
    "id": 1,
    "username": "admin",
    "nombres": "Admin",
    "apellidos": "Sistema",
    "id_proveedor": null,
    "estado": true,
    "rol_id": 1,
    "created_at": "2024-12-10T10:30:00Z",
    "updated_at": null
  },
  {
    "id": 2,
    "username": "vendedor1",
    "nombres": "Juan",
    "apellidos": "Pérez",
    "id_proveedor": null,
    "estado": true,
    "rol_id": 2,
    "created_at": "2024-12-10T11:00:00Z",
    "updated_at": null
  }
]
```

---

### GET `/api/v1/users/{user_id}`

Obtiene un usuario por su ID.

#### Path Parameters

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `user_id` | int | ID del usuario |

#### Ejemplo Request

```javascript
const userId = 1;
const response = await fetch(`http://localhost:8000/api/v1/users/${userId}`, {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});
```

#### Response 200 OK

```json
{
  "id": 1,
  "username": "admin",
  "nombres": "Admin",
  "apellidos": "Sistema",
  "id_proveedor": null,
  "estado": true,
  "rol_id": 1,
  "created_at": "2024-12-10T10:30:00Z",
  "updated_at": null
}
```

#### Errores

| Código | Descripción |
|--------|-------------|
| 404 | Usuario no encontrado |

---

### POST `/api/v1/users`

Crea un nuevo usuario.

#### Request Body

**Content-Type:** `application/json`

| Campo | Tipo | Requerido | Validación | Descripción |
|-------|------|-----------|------------|-------------|
| `username` | string | ✅ | 3-50 chars | Nombre de usuario único |
| `password` | string | ✅ | min 8 chars | Contraseña |
| `nombres` | string | ✅ | 1-100 chars | Nombres |
| `apellidos` | string | ✅ | 1-100 chars | Apellidos |
| `rol_id` | int | ✅ | > 0 | ID del rol |
| `id_proveedor` | int | ❌ | | ID del proveedor (opcional) |

#### Ejemplo Request

```javascript
const response = await fetch('http://localhost:8000/api/v1/users/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: 'nuevo_usuario',
    password: 'password123',
    nombres: 'Juan',
    apellidos: 'Pérez García',
    rol_id: 1,
    id_proveedor: null
  })
});
```

#### Response 201 Created

```json
{
  "id": 3,
  "username": "nuevo_usuario",
  "nombres": "Juan",
  "apellidos": "Pérez García",
  "id_proveedor": null,
  "estado": true,
  "rol_id": 1,
  "created_at": "2024-12-10T12:00:00Z",
  "updated_at": null
}
```

#### Errores

| Código | Descripción |
|--------|-------------|
| 400 | Username ya existe |
| 422 | Error de validación |

---

### PATCH `/api/v1/users/{user_id}`

Actualiza un usuario (campos parciales).

#### Request Body

**Content-Type:** `application/json`

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `nombres` | string | ❌ | Nombres |
| `apellidos` | string | ❌ | Apellidos |
| `id_proveedor` | int | ❌ | ID del proveedor |
| `estado` | bool | ❌ | Estado activo/inactivo |
| `rol_id` | int | ❌ | ID del rol |

#### Ejemplo Request

```javascript
const userId = 2;
const response = await fetch(`http://localhost:8000/api/v1/users/${userId}`, {
  method: 'PATCH',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    nombres: 'Juan Carlos',
    estado: true
  })
});
```

#### Response 200 OK

```json
{
  "id": 2,
  "username": "vendedor1",
  "nombres": "Juan Carlos",
  "apellidos": "Pérez",
  "id_proveedor": null,
  "estado": true,
  "rol_id": 2,
  "created_at": "2024-12-10T11:00:00Z",
  "updated_at": "2024-12-10T13:00:00Z"
}
```

---

### DELETE `/api/v1/users/{user_id}`

Desactiva un usuario (soft delete).

#### Ejemplo Request

```javascript
const userId = 2;
const response = await fetch(`http://localhost:8000/api/v1/users/${userId}`, {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});
```

#### Response 200 OK

```json
{
  "message": "Usuario desactivado correctamente"
}
```

---

### POST `/api/v1/users/{user_id}/change-password`

Cambia la contraseña de un usuario.

#### Request Body

**Content-Type:** `application/json`

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `current_password` | string | ✅ | Contraseña actual |
| `new_password` | string | ✅ | Nueva contraseña (min 8 chars) |

#### Ejemplo Request

```javascript
const userId = 1;
const response = await fetch(`http://localhost:8000/api/v1/users/${userId}/change-password`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    current_password: 'admin123',
    new_password: 'nuevaPassword456'
  })
});
```

#### Response 200 OK

```json
{
  "message": "Contraseña actualizada correctamente"
}
```

#### Errores

| Código | Descripción |
|--------|-------------|
| 400 | Contraseña actual incorrecta |

---

## 🏷️ Endpoints de Roles

> ⚠️ **Todos estos endpoints requieren autenticación**

### GET `/api/v1/roles`

Lista todos los roles.

#### Ejemplo Request

```javascript
const response = await fetch('http://localhost:8000/api/v1/roles/', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});
```

#### Response 200 OK

```json
[
  {
    "id_rol": 1,
    "nombre_rol": "Administrador",
    "descripcion": "Rol con todos los permisos",
    "created_at": "2024-12-10T10:00:00Z",
    "updated_at": null
  },
  {
    "id_rol": 2,
    "nombre_rol": "Vendedor",
    "descripcion": "Rol para vendedores",
    "created_at": "2024-12-10T10:30:00Z",
    "updated_at": null
  }
]
```

---

### GET `/api/v1/roles/{role_id}`

Obtiene un rol por su ID.

#### Ejemplo Request

```javascript
const roleId = 1;
const response = await fetch(`http://localhost:8000/api/v1/roles/${roleId}`, {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});
```

#### Response 200 OK

```json
{
  "id_rol": 1,
  "nombre_rol": "Administrador",
  "descripcion": "Rol con todos los permisos",
  "created_at": "2024-12-10T10:00:00Z",
  "updated_at": null
}
```

---

### POST `/api/v1/roles`

Crea un nuevo rol.

#### Request Body

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `nombre_rol` | string | ✅ | Nombre del rol (1-50 chars) |
| `descripcion` | string | ❌ | Descripción del rol |

#### Ejemplo Request

```javascript
const response = await fetch('http://localhost:8000/api/v1/roles/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    nombre_rol: 'Cajero',
    descripcion: 'Rol para cajeros de la tienda'
  })
});
```

#### Response 201 Created

```json
{
  "id_rol": 3,
  "nombre_rol": "Cajero",
  "descripcion": "Rol para cajeros de la tienda",
  "created_at": "2024-12-10T14:00:00Z",
  "updated_at": null
}
```

---

### PATCH `/api/v1/roles/{role_id}`

Actualiza un rol.

#### Request Body

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `nombre_rol` | string | ❌ | Nombre del rol |
| `descripcion` | string | ❌ | Descripción |

#### Ejemplo Request

```javascript
const roleId = 3;
const response = await fetch(`http://localhost:8000/api/v1/roles/${roleId}`, {
  method: 'PATCH',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    descripcion: 'Rol actualizado para cajeros principales'
  })
});
```

#### Response 200 OK

```json
{
  "id_rol": 3,
  "nombre_rol": "Cajero",
  "descripcion": "Rol actualizado para cajeros principales",
  "created_at": "2024-12-10T14:00:00Z",
  "updated_at": "2024-12-10T15:00:00Z"
}
```

---

## 📦 Endpoints de Inventario Excluido

> ⚠️ **Todos estos endpoints requieren autenticación**

Gestiona los productos que deben ser excluidos del inventario.

### GET `/api/v1/inventario-excluido`

Lista todos los registros de inventario excluido con paginación.

#### Query Parameters

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `skip` | int | 0 | Registros a saltar (paginación) |
| `limit` | int | 100 | Máximo de registros |
| `include_inactive` | bool | false | Incluir registros inactivos |

#### Ejemplo Request

```javascript
const response = await fetch('http://localhost:8000/api/v1/inventario-excluido?skip=0&limit=10&include_inactive=false', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});
```

#### Response 200 OK

```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "codigo_producto": "PROD-001",
      "empresa": "Ferreteria Central",
      "status": true,
      "created_at": "2024-12-10T10:30:00Z",
      "updated_at": null
    },
    {
      "id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
      "codigo_producto": "PROD-002",
      "empresa": "Ferreteria Central",
      "status": true,
      "created_at": "2024-12-10T11:00:00Z",
      "updated_at": null
    }
  ],
  "total": 2,
  "skip": 0,
  "limit": 10
}
```

---

### GET `/api/v1/inventario-excluido/{record_id}`

Obtiene un registro de inventario excluido por su UUID.

#### Path Parameters

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `record_id` | UUID | ID único del registro |

#### Ejemplo Request

```javascript
const recordId = '550e8400-e29b-41d4-a716-446655440000';
const response = await fetch(`http://localhost:8000/api/v1/inventario-excluido/${recordId}`, {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});
```

#### Response 200 OK

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "codigo_producto": "PROD-001",
  "empresa": "Ferreteria Central",
  "status": true,
  "created_at": "2024-12-10T10:30:00Z",
  "updated_at": null
}
```

#### Errores

| Código | Descripción |
|--------|-------------|
| 404 | Registro no encontrado |

---

### POST `/api/v1/inventario-excluido`

Crea un nuevo registro de producto excluido.

#### Request Body

**Content-Type:** `application/json`

| Campo | Tipo | Requerido | Validación | Descripción |
|-------|------|-----------|------------|-------------|
| `codigo_producto` | string | ✅ | 1-100 chars | Código del producto a excluir |
| `empresa` | string | ✅ | 1-100 chars | Empresa a la que pertenece el producto |
| `status` | bool | ❌ | | Estado del registro (default: true) |

> ⚠️ La combinación `empresa` + `codigo_producto` debe ser única.

#### Ejemplo Request

```javascript
const response = await fetch('http://localhost:8000/api/v1/inventario-excluido/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    codigo_producto: 'PROD-003',
    empresa: 'Ferreteria Central',
    status: true
  })
});
```

#### Response 201 Created

```json
{
  "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "codigo_producto": "PROD-003",
  "empresa": "Ferreteria Central",
  "status": true,
  "created_at": "2024-12-10T12:00:00Z",
  "updated_at": null
}
```

#### Errores

| Código | Descripción |
|--------|-------------|
| 400 | Combinación empresa + código de producto ya existe |
| 422 | Error de validación |

---

### PATCH `/api/v1/inventario-excluido/{record_id}`

Actualiza un registro de inventario excluido.

#### Path Parameters

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `record_id` | UUID | ID único del registro |

#### Request Body

**Content-Type:** `application/json`

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `codigo_producto` | string | ❌ | Nuevo código del producto |
| `empresa` | string | ❌ | Nueva empresa |
| `status` | bool | ❌ | Nuevo estado |

#### Ejemplo Request

```javascript
const recordId = '550e8400-e29b-41d4-a716-446655440000';
const response = await fetch(`http://localhost:8000/api/v1/inventario-excluido/${recordId}`, {
  method: 'PATCH',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    codigo_producto: 'PROD-001-UPDATED'
  })
});
```

#### Response 200 OK

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "codigo_producto": "PROD-001-UPDATED",
  "empresa": "Ferreteria Central",
  "status": true,
  "created_at": "2024-12-10T10:30:00Z",
  "updated_at": "2024-12-10T14:00:00Z"
}
```

---

### PATCH `/api/v1/inventario-excluido/{record_id}/toggle-status`

Cambia el estado de un registro (activo/inactivo).

#### Path Parameters

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `record_id` | UUID | ID único del registro |

#### Request Body

**Content-Type:** `application/json`

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `status` | bool | ✅ | Nuevo estado (true=activo, false=inactivo) |

#### Ejemplo Request

```javascript
const recordId = '550e8400-e29b-41d4-a716-446655440000';
const response = await fetch(`http://localhost:8000/api/v1/inventario-excluido/${recordId}/toggle-status`, {
  method: 'PATCH',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    status: false
  })
});
```

#### Response 200 OK

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "codigo_producto": "PROD-001",
  "empresa": "Ferreteria Central",
  "status": false,
  "created_at": "2024-12-10T10:30:00Z",
  "updated_at": "2024-12-10T15:00:00Z"
}
```

---

### DELETE `/api/v1/inventario-excluido/{record_id}`

Elimina permanentemente un registro de inventario excluido.

> ⚠️ **Advertencia:** Esta operación es irreversible.

#### Path Parameters

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `record_id` | UUID | ID único del registro a eliminar |

#### Ejemplo Request

```javascript
const recordId = '550e8400-e29b-41d4-a716-446655440000';
const response = await fetch(`http://localhost:8000/api/v1/inventario-excluido/${recordId}`, {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});
```

#### Response 200 OK

```json
{
  "message": "Registro eliminado correctamente"
}
```

#### Errores

| Código | Descripción |
|--------|-------------|
| 404 | Registro no encontrado |

---

## 📅 Endpoints de Días de Entrega por Proveedor

> ⚠️ **Todos estos endpoints requieren autenticación**

Gestiona los días de entrega configurados por proveedor y empresa.

### GET `/api/v1/dias-entrega-proveedor`

Lista todos los registros de días de entrega con paginación.

#### Query Parameters

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `skip` | int | 0 | Registros a saltar (paginación) |
| `limit` | int | 100 | Máximo de registros |
| `empresa` | string | null | Filtrar por empresa (opcional) |

#### Ejemplo Request

```javascript
const response = await fetch('http://localhost:8000/api/v1/dias-entrega-proveedor?skip=0&limit=10&empresa=Ferreteria Central', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});
```

#### Response 200 OK

```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "empresa": "Ferreteria Central",
      "nit_proveedor": "900123456-1",
      "dias_entrega": 5
    },
    {
      "id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
      "empresa": "Ferreteria Central",
      "nit_proveedor": "800987654-2",
      "dias_entrega": 3
    }
  ],
  "total": 2,
  "skip": 0,
  "limit": 10
}
```

---

### GET `/api/v1/dias-entrega-proveedor/{record_id}`

Obtiene un registro de días de entrega por su UUID.

#### Path Parameters

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `record_id` | UUID | ID único del registro |

#### Ejemplo Request

```javascript
const recordId = '550e8400-e29b-41d4-a716-446655440000';
const response = await fetch(`http://localhost:8000/api/v1/dias-entrega-proveedor/${recordId}`, {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});
```

#### Response 200 OK

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "empresa": "Ferreteria Central",
  "nit_proveedor": "900123456-1",
  "dias_entrega": 5
}
```

#### Errores

| Código | Descripción |
|--------|-------------|
| 404 | Registro no encontrado |

---

### POST `/api/v1/dias-entrega-proveedor`

Crea un nuevo registro de días de entrega por proveedor.

#### Request Body

**Content-Type:** `application/json`

| Campo | Tipo | Requerido | Validación | Descripción |
|-------|------|-----------|------------|-------------|
| `empresa` | string | ✅ | 1-100 chars | Código o nombre de la empresa |
| `nit_proveedor` | string | ✅ | 1-200 chars | NIT o identificación del proveedor |
| `dias_entrega` | int | ✅ | >= 0 | Cantidad de días estimados de entrega |

> ⚠️ La combinación `empresa` + `nit_proveedor` debe ser única.

#### Ejemplo Request

```javascript
const response = await fetch('http://localhost:8000/api/v1/dias-entrega-proveedor/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    empresa: 'Ferreteria Central',
    nit_proveedor: '900123456-1',
    dias_entrega: 5
  })
});
```

#### Response 201 Created

```json
{
  "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "empresa": "Ferreteria Central",
  "nit_proveedor": "900123456-1",
  "dias_entrega": 5
}
```

#### Errores

| Código | Descripción |
|--------|-------------|
| 400 | Combinación empresa + NIT proveedor ya existe |
| 422 | Error de validación |

---

### PATCH `/api/v1/dias-entrega-proveedor/{record_id}`

Actualiza un registro de días de entrega.

#### Path Parameters

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `record_id` | UUID | ID único del registro |

#### Request Body

**Content-Type:** `application/json`

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `empresa` | string | ❌ | Nueva empresa |
| `nit_proveedor` | string | ❌ | Nuevo NIT del proveedor |
| `dias_entrega` | int | ❌ | Nueva cantidad de días |

#### Ejemplo Request

```javascript
const recordId = '550e8400-e29b-41d4-a716-446655440000';
const response = await fetch(`http://localhost:8000/api/v1/dias-entrega-proveedor/${recordId}`, {
  method: 'PATCH',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    dias_entrega: 7
  })
});
```

#### Response 200 OK

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "empresa": "Ferreteria Central",
  "nit_proveedor": "900123456-1",
  "dias_entrega": 7
}
```

---

### DELETE `/api/v1/dias-entrega-proveedor/{record_id}`

Elimina permanentemente un registro de días de entrega.

> ⚠️ **Advertencia:** Esta operación es irreversible.

#### Path Parameters

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `record_id` | UUID | ID único del registro a eliminar |

#### Ejemplo Request

```javascript
const recordId = '550e8400-e29b-41d4-a716-446655440000';
const response = await fetch(`http://localhost:8000/api/v1/dias-entrega-proveedor/${recordId}`, {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});
```

#### Response 200 OK

```json
{
  "message": "Registro eliminado exitosamente"
}
```

#### Errores

| Código | Descripción |
|--------|-------------|
| 404 | Registro no encontrado |

---

## 📦 Endpoints de Vista Inventarios

> ⚠️ **Todos estos endpoints requieren autenticación**

Consulta la tabla de inventarios con información básica de productos.

### GET `/api/v1/vista-inventarios`

Lista todos los productos del inventario con campos básicos (empresa, código de producto y descripción).

#### Query Parameters

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `skip` | int | 0 | Registros a saltar (paginación) |
| `limit` | int | 100 | Máximo de registros a retornar |
| `empresa` | string | null | Filtrar por empresa (opcional) |

#### Ejemplo Request (JavaScript/Fetch)

```javascript
// Sin filtro de empresa
const response = await fetch('http://localhost:8000/api/v1/vista-inventarios?skip=0&limit=50', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});

const data = await response.json();
console.log(data.items); // Array de productos
console.log(data.total); // Total de productos
```

#### Ejemplo Request con filtro de empresa

```javascript
// Con filtro de empresa
const empresa = 'Ferreteria Central';
const response = await fetch(`http://localhost:8000/api/v1/vista-inventarios?skip=0&limit=50&empresa=${encodeURIComponent(empresa)}`, {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});
```

#### Ejemplo Request (Axios)

```javascript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});

// Sin filtro
const response = await apiClient.get('/vista-inventarios', {
  params: {
    skip: 0,
    limit: 50
  }
});

// Con filtro de empresa
const responseFiltered = await apiClient.get('/vista-inventarios', {
  params: {
    skip: 0,
    limit: 50,
    empresa: 'Ferreteria Central'
  }
});
```

#### Response 200 OK

```json
{
  "items": [
    {
      "empresa": "Ferreteria Central",
      "codigo_producto": "CLAVO-2P",
      "descripcion": "Clavo de 2 pulgadas caja x 100"
    },
    {
      "empresa": "Ferreteria Central",
      "codigo_producto": "MART-500G",
      "descripcion": "Martillo de 500 gramos mango de madera"
    },
    {
      "empresa": "Ferreteria Central",
      "codigo_producto": "TORN-M8",
      "descripcion": "Tornillo M8 x 50mm acero inoxidable"
    }
  ],
  "total": 1250,
  "skip": 0,
  "limit": 50
}
```

#### Paginación

La respuesta incluye información de paginación:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `items` | array | Lista de productos en la página actual |
| `total` | int | Total de productos (para calcular páginas) |
| `skip` | int | Registros saltados |
| `limit` | int | Límite aplicado |

**Ejemplo de cálculo de páginas:**

```javascript
const pageSize = 50;
const currentPage = 1; // Páginas empiezan en 1

const response = await fetch(`http://localhost:8000/api/v1/vista-inventarios?skip=${(currentPage - 1) * pageSize}&limit=${pageSize}`, {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});

const data = await response.json();

// Calcular total de páginas
const totalPages = Math.ceil(data.total / pageSize);
console.log(`Página ${currentPage} de ${totalPages}`);
```

#### Errores

| Código | Descripción |
|--------|-------------|
| 401 | Token inválido o expirado |
| 422 | Error de validación en parámetros |

---

## ❌ Manejo de Errores

### Estructura de Error

```json
{
  "detail": "Mensaje descriptivo del error"
}
```

### Códigos HTTP Comunes

| Código | Significado | Cuándo ocurre |
|--------|-------------|---------------|
| 200 | OK | Petición exitosa |
| 201 | Created | Recurso creado exitosamente |
| 400 | Bad Request | Datos inválidos o lógica de negocio |
| 401 | Unauthorized | Token inválido o expirado |
| 403 | Forbidden | Sin permisos para la acción |
| 404 | Not Found | Recurso no encontrado |
| 422 | Unprocessable Entity | Error de validación de datos |
| 500 | Internal Server Error | Error del servidor |

### Manejo Recomendado (JavaScript)

```javascript
// Interceptor para manejar tokens expirados
async function fetchWithAuth(url, options = {}) {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}`
    }
  });

  // Si el token expiró, intentar renovar
  if (response.status === 401) {
    const refreshed = await refreshToken();
    if (refreshed) {
      // Reintentar con nuevo token
      return fetchWithAuth(url, options);
    } else {
      // Redirigir a login
      window.location.href = '/login';
      return null;
    }
  }

  return response;
}

async function refreshToken() {
  try {
    const refresh = localStorage.getItem('refresh_token');
    const response = await fetch('http://localhost:8000/api/v1/auth/refresh-token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refresh })
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('access_token', data.access_token);
      return true;
    }
    return false;
  } catch {
    return false;
  }
}
```

---

## 🔧 Configuración CORS

La API permite peticiones desde cualquier origen en desarrollo. Headers permitidos:

```javascript
// Configuración actual del backend
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: *
Access-Control-Allow-Credentials: true
```

---

## 📦 Modelos de Datos

### Usuario (UserResponse)

```typescript
interface User {
  id: number;
  username: string;
  nombres: string;
  apellidos: string;
  id_proveedor: number | null;
  estado: boolean;
  rol_id: number;
  created_at: string; // ISO 8601
  updated_at: string | null;
}
```

### Rol (RoleResponse)

```typescript
interface Role {
  id_rol: number;
  nombre_rol: string;
  descripcion: string | null;
  created_at: string;
  updated_at: string | null;
}
```

### Token

```typescript
interface Token {
  access_token: string;
  refresh_token: string;
  token_type: "bearer";
}
```

### Inventario Excluido (InventarioExcluidoResponse)

```typescript
interface InventarioExcluido {
  id: string;           // UUID
  codigo_producto: string;
  empresa: string;
  status: boolean;
  created_at: string;   // ISO 8601
  updated_at: string | null;
}

interface InventarioExcluidoListResponse {
  items: InventarioExcluido[];
  total: number;
  skip: number;
  limit: number;
}
```

### Días Entrega Proveedor (DiasEntregaProveedorResponse)

```typescript
interface DiasEntregaProveedor {
  id: string;           // UUID
  empresa: string;
  nit_proveedor: string;
  dias_entrega: number;
}

interface DiasEntregaProveedorListResponse {
  items: DiasEntregaProveedor[];
  total: number;
  skip: number;
  limit: number;
}
```

### Vista Inventarios (VistaInventarioItem)

```typescript
interface VistaInventarioItem {
  empresa: string;
  codigo_producto: string;
  descripcion: string;
}

interface VistaInventariosListResponse {
  items: VistaInventarioItem[];
  total: number;
  skip: number;
  limit: number;
}
```

---

## 🚀 Ejemplo Completo: Servicio de Autenticación (React/TypeScript)

```typescript
// services/authService.ts
const API_URL = 'http://localhost:8000/api/v1';

interface LoginCredentials {
  username: string;
  password: string;
}

interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

interface User {
  id: number;
  username: string;
  nombres: string;
  apellidos: string;
  estado: boolean;
  rol_id: number;
}

class AuthService {
  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Error de autenticación');
    }

    const data = await response.json();
    this.setTokens(data);
    return data;
  }

  async getCurrentUser(): Promise<User> {
    const response = await fetch(`${API_URL}/users/me`, {
      headers: {
        'Authorization': `Bearer ${this.getAccessToken()}`,
      },
    });

    if (!response.ok) {
      throw new Error('Error al obtener usuario');
    }

    return response.json();
  }

  async refreshToken(): Promise<boolean> {
    try {
      const response = await fetch(`${API_URL}/auth/refresh-token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          refresh_token: this.getRefreshToken(),
        }),
      });

      if (response.ok) {
        const data = await response.json();
        this.setTokens(data);
        return true;
      }
      return false;
    } catch {
      return false;
    }
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  isAuthenticated(): boolean {
    return !!this.getAccessToken();
  }

  private setTokens(tokens: TokenResponse): void {
    localStorage.setItem('access_token', tokens.access_token);
    localStorage.setItem('refresh_token', tokens.refresh_token);
  }

  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

  private getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token');
  }
}

export const authService = new AuthService();
```

---

## 📞 Contacto

Para dudas técnicas sobre la API, consultar la documentación interactiva en:
- **Swagger:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

