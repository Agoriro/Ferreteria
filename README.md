# Ferretería API - Backend

API REST con arquitectura hexagonal (Ports & Adapters) para sistema de ferretería.

## 🛠️ Tecnologías

- **FastAPI** 0.115.0 - Framework web
- **SQLAlchemy** 2.0 (async) - ORM
- **PostgreSQL** - Base de datos
- **JWT** - Autenticación
- **Bcrypt** - Hash de contraseñas
- **Pydantic** 2.10 - Validación de datos

## 📁 Estructura del Proyecto

```
src/
├── domain/           # Capa de dominio
│   ├── entities/     # Entidades del negocio
│   ├── ports/        # Interfaces (puertos)
│   └── schemas/      # DTOs (Pydantic)
├── application/      # Capa de aplicación
│   ├── services/     # Servicios de dominio
│   └── use_cases/    # Casos de uso
├── infrastructure/   # Capa de infraestructura
│   ├── adapters/     # Adaptadores (web, repositorios)
│   ├── config/       # Configuración
│   ├── models/       # Modelos SQLAlchemy
│   └── security/     # JWT handler
└── main.py           # Punto de entrada
```

## 🚀 Instalación y Configuración

### 1. Prerrequisitos

- Python 3.10+
- PostgreSQL 12+
- pip o pipenv

### 2. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd Ferreteria
```

### 3. Crear entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en Linux/Mac
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Database Configuration
DATABASE_URL=postgresql://usuario:password@localhost:5432/ferreteria_db

# JWT Configuration
SECRET_KEY=tu_clave_secreta_muy_segura_cambiar_en_produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# App Configuration
APP_NAME=Hexagonal Auth API
DEBUG=True
```

### 6. Crear base de datos PostgreSQL

```sql
-- Conectar a PostgreSQL y ejecutar:
CREATE DATABASE ferreteria_db;
```

### 7. Ejecutar migraciones con Alembic

```bash
# Generar migración inicial (si no existe)
alembic revision --autogenerate -m "Initial migration"

# Aplicar migraciones
alembic upgrade head
```

### 8. Crear usuario inicial (opcional)

Puedes crear un usuario administrador inicial directamente en la BD:

```sql
-- Primero crear un rol
INSERT INTO roles (nombre_rol, descripcion) 
VALUES ('Administrador', 'Rol con todos los permisos');

-- Crear usuario admin (password: admin123 - hasheado con bcrypt)
INSERT INTO usuarios (username, password, nombres, apellidos, rol_id, estado)
VALUES (
    'admin', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.V1rTqBR5jKKJWe',
    'Admin', 
    'Sistema',
    1,
    true
);
```

## ▶️ Ejecutar el Proyecto

### Opción 1: Con uvicorn directamente

```bash
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Opción 2: Ejecutar main.py

```bash
cd src
python main.py
```

### Verificar que funciona

- **API Docs (Swagger):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

## 📬 Colección de Postman

En la carpeta `postman/` encontrarás:

- `Ferreteria_API.postman_collection.json` - Colección con todos los endpoints
- `Ferreteria_API.postman_environment.json` - Variables de entorno

### Importar en Postman

1. Abrir Postman
2. Click en **Import**
3. Seleccionar ambos archivos JSON de la carpeta `postman/`
4. Seleccionar el environment "Ferreteria - Local"

### Flujo de pruebas

1. **Health Check** - Verificar que la API está corriendo
2. **Login** - Autenticarse (guarda tokens automáticamente)
3. **Probar endpoints** - Los demás endpoints usan el token guardado

## 📋 Endpoints Disponibles

### Authentication
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/auth/login` | Iniciar sesión |
| POST | `/api/v1/auth/refresh-token` | Renovar access token |

### Users
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/users/` | Crear usuario |
| GET | `/api/v1/users/` | Listar usuarios |
| GET | `/api/v1/users/me` | Usuario actual |
| GET | `/api/v1/users/{id}` | Obtener usuario |
| PATCH | `/api/v1/users/{id}` | Actualizar usuario |
| DELETE | `/api/v1/users/{id}` | Eliminar usuario (soft) |
| POST | `/api/v1/users/{id}/change-password` | Cambiar contraseña |

### Roles
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/roles/` | Crear rol |
| GET | `/api/v1/roles/` | Listar roles |
| GET | `/api/v1/roles/{id}` | Obtener rol |
| PATCH | `/api/v1/roles/{id}` | Actualizar rol |

### Health
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Health check básico |
| GET | `/health` | Estado de salud |

## 🔐 Autenticación

La API usa JWT (JSON Web Tokens):

1. **Login:** Enviar `username` y `password` como `application/x-www-form-urlencoded`
2. **Respuesta:** Recibes `access_token` y `refresh_token`
3. **Usar endpoints protegidos:** Agregar header `Authorization: Bearer <access_token>`
4. **Renovar token:** Cuando expire el access_token, usar `/auth/refresh-token`

## 🏗️ Arquitectura Hexagonal

```
┌─────────────────────────────────────────────────────────────┐
│                     INFRASTRUCTURE                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   FastAPI   │  │  SQLAlchemy │  │    JWT Handler      │ │
│  │   Routers   │  │   Repos     │  │                     │ │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘ │
└─────────┼────────────────┼───────────────────┼─────────────┘
          │                │                   │
          ▼                ▼                   ▼
┌─────────────────────────────────────────────────────────────┐
│                      APPLICATION                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                    Use Cases                           │ │
│  │   AuthUseCase  │  UserUseCase  │  RoleUseCase         │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
          │                │                   │
          ▼                ▼                   ▼
┌─────────────────────────────────────────────────────────────┐
│                        DOMAIN                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  Entities   │  │    Ports    │  │      Schemas        │ │
│  │             │  │ (Interfaces)│  │      (DTOs)         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 📝 Licencia

MIT

