# Guía de Despliegue en Render

## Requisitos Previos
- Cuenta en [GitHub](https://github.com)
- Cuenta en [Render](https://render.com)
- Tu base de datos Supabase ya configurada

---

## Paso 1: Subir el Código a GitHub

```bash
# Inicializar git (si no está inicializado)
git init

# Agregar archivos (el .gitignore excluye .env automáticamente)
git add .

# Commit inicial
git commit -m "Initial commit - Ferreteria API"

# Crear repo en GitHub y conectar
git remote add origin https://github.com/TU_USUARIO/ferreteria-api.git
git branch -M main
git push -u origin main
```

---

## Paso 2: Crear Web Service en Render

1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu cuenta de GitHub
4. Selecciona el repositorio `ferreteria-api`
5. Configura:

| Campo | Valor |
|-------|-------|
| **Name** | `ferreteria-api` |
| **Region** | `Oregon (US West)` o el más cercano |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `cd src && uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` |

---

## Paso 3: Configurar Variables de Entorno

En la sección **"Environment"** de Render, agrega estas variables:

| Variable | Valor | Notas |
|----------|-------|-------|
| `DATABASE_URL` | `postgresql://postgres.xxx:password@host:5432/postgres` | Tu URL de Supabase |
| `SECRET_KEY` | `tu_clave_secreta_muy_larga` | Genera una nueva con `openssl rand -hex 32` |
| `ALGORITHM` | `HS256` | |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` | |
| `APP_NAME` | `Ferreteria API` | |
| `DEBUG` | `false` | **Importante**: false en producción |
| `CORS_ORIGINS` | `https://tu-frontend.vercel.app,http://localhost:5173` | URLs de tu frontend |
| `PYTHON_VERSION` | `3.11.0` | |

---

## Paso 4: Desplegar

1. Click en **"Create Web Service"**
2. Render clonará tu repo y desplegará automáticamente
3. Espera 2-5 minutos para el build inicial
4. Tu API estará disponible en: `https://ferreteria-api.onrender.com`

---

## Paso 5: Verificar el Despliegue

```bash
# Health check
curl https://ferreteria-api.onrender.com/health

# Documentación API
# Abre en navegador: https://ferreteria-api.onrender.com/docs
```

---

## Notas Importantes

### 🔄 Despliegue Automático
Cada vez que hagas `git push` a la rama `main`, Render re-desplegará automáticamente.

### 😴 Modo Sleep (Plan Gratis)
- El servicio se "duerme" después de 15 minutos de inactividad
- La primera request después de dormir toma ~30 segundos
- Solución: Usar un servicio de ping como [UptimeRobot](https://uptimerobot.com) (gratis)

### 🔒 Seguridad
- **NUNCA** subas el archivo `.env` a GitHub
- Genera un nuevo `SECRET_KEY` para producción
- Cambia la contraseña de tu base de datos Supabase si la expusiste

---

## Comandos Útiles

```bash
# Generar nueva SECRET_KEY
openssl rand -hex 32

# Ver logs en Render
# Ve a: Dashboard → Tu servicio → Logs
```

---

## Estructura de URLs

| Ambiente | URL |
|----------|-----|
| **Producción** | `https://ferreteria-api.onrender.com` |
| **Docs** | `https://ferreteria-api.onrender.com/docs` |
| **Health** | `https://ferreteria-api.onrender.com/health` |
