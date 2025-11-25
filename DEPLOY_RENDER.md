# 🚀 Plan de Deploy: GitHub + Render.com

Guía paso a paso para subir Ahorify V1.5 a GitHub y desplegarlo en Render.com.

---

## 📋 PARTE 1: SUBIR A GITHUB

### Paso 1: Verificar que no hay archivos sensibles

```bash
cd "/Users/tristansepulvedacebrian/Desktop/ahorify v.1.5"

# Verificar que .env no esté en el staging
git status

# Si aparece .env, asegúrate de que esté en .gitignore
# Los archivos .env.example SÍ deben estar en el repo
```

### Paso 2: Inicializar Git (si no está inicializado)

```bash
# Verificar si ya es un repo git
git status

# Si no es un repo, inicializar:
git init
```

### Paso 3: Agregar todos los archivos

```bash
# Agregar todos los archivos (excepto los ignorados en .gitignore)
git add .

# Verificar qué se va a subir
git status
```

### Paso 4: Hacer commit inicial

```bash
git commit -m "Initial commit: Ahorify V1.5 - Listo para deploy"
```

### Paso 5: Crear repositorio en GitHub

1. Ve a [GitHub.com](https://github.com) e inicia sesión
2. Click en **"New repository"** (botón verde o +)
3. Configura:
   - **Repository name**: `ahorify` (o el nombre que prefieras)
   - **Description**: "PWA Mobile-First para gestión de finanzas personales"
   - **Visibility**: Private (recomendado) o Public
   - **NO marques** "Initialize with README" (ya tienes uno)
4. Click en **"Create repository"**

### Paso 6: Conectar y subir a GitHub

```bash
# Agregar el remote (reemplaza TU_USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU_USUARIO/ahorify.git

# O si prefieres SSH:
# git remote add origin git@github.com:TU_USUARIO/ahorify.git

# Verificar el remote
git remote -v

# Subir el código
git branch -M main
git push -u origin main
```

**Nota sobre autenticación:**
- **HTTPS**: Necesitarás un Personal Access Token (Settings > Developer settings > Personal access tokens)
- **SSH**: Configura tus llaves SSH primero

---

## 📋 PARTE 2: CONFIGURAR RENDER.COM

### Paso 7: Crear cuenta en Render.com

1. Ve a [Render.com](https://render.com)
2. Click en **"Get Started for Free"**
3. Regístrate con GitHub (recomendado) o email
4. Conecta tu cuenta de GitHub si usaste email

### Paso 8: Crear Base de Datos PostgreSQL

1. En el Dashboard de Render, click en **"New +"**
2. Selecciona **"PostgreSQL"**
3. Configura:
   - **Name**: `ahorify-db`
   - **Database**: `ahorify` (o déjalo por defecto)
   - **User**: Se genera automáticamente
   - **Region**: Elige la más cercana (ej: `Oregon (US West)`)
   - **PostgreSQL Version**: `16` (o la más reciente)
   - **Plan**: `Free` (para empezar)
4. Click en **"Create Database"**
5. **IMPORTANTE**: Guarda la **Internal Database URL** que aparece (la necesitarás después)
   - Formato: `postgresql://usuario:password@dpg-xxxxx-a/ahorify`
   - ⚠️ Usa la **Internal Database URL**, no la externa

---

## 📋 PARTE 3: DESPLEGAR BACKEND EN RENDER

### Paso 9: Crear Web Service para Backend

1. En Render Dashboard, click en **"New +"**
2. Selecciona **"Web Service"**
3. Conecta tu repositorio de GitHub:
   - Si no está conectado, click en **"Connect account"**
   - Selecciona el repositorio `ahorify`
   - Click en **"Connect"**
4. Configura el servicio:
   - **Name**: `ahorify-api`
   - **Region**: Misma que la base de datos
   - **Branch**: `main`
   - **Root Directory**: `backend` ⚠️ **IMPORTANTE**
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
     ```
   - **Plan**: `Free` (para empezar)

### Paso 10: Configurar Variables de Entorno del Backend

En la sección **"Environment Variables"** del servicio, agrega:

```env
ENVIRONMENT=production

# Base de datos (usa la Internal Database URL de Render)
DATABASE_URL=postgresql://usuario:password@dpg-xxxxx-a/ahorify

# Google OAuth (tu Client ID)
GOOGLE_CLIENT_ID=tu-google-client-id.apps.googleusercontent.com

# CORS (actualiza después con la URL real de Render)
ALLOWED_ORIGINS=https://ahorify-frontend.onrender.com

# Waitlist
WAITLIST_LIMIT=50
```

**Nota**: Render asigna una URL automáticamente como `ahorify-api.onrender.com`. Puedes actualizar `ALLOWED_ORIGINS` después de crear el frontend.

### Paso 11: Verificar que el Backend funciona

1. Render iniciará el deploy automáticamente
2. Espera a que termine (puede tardar 2-5 minutos)
3. Ve a la URL del servicio (ej: `https://ahorify-api.onrender.com`)
4. Deberías ver el health check:
   ```json
   {
     "status": "healthy",
     "database": "✅ Connected",
     "version": "1.5.0",
     "timestamp": "..."
   }
   ```
5. Ve a `https://ahorify-api.onrender.com/docs` para ver la documentación

---

## 📋 PARTE 4: DESPLEGAR FRONTEND EN RENDER

### Paso 12: Crear Static Site para Frontend

1. En Render Dashboard, click en **"New +"**
2. Selecciona **"Static Site"**
3. Conecta el mismo repositorio:
   - Selecciona `ahorify`
   - Click en **"Connect"**
4. Configura:
   - **Name**: `ahorify-frontend`
   - **Branch**: `main`
   - **Root Directory**: `frontend` ⚠️ **IMPORTANTE**
   - **Build Command**: 
     ```bash
     npm install && npm run build
     ```
   - **Publish Directory**: `dist`
   - **Plan**: `Free`

### Paso 13: Configurar Variables de Entorno del Frontend

En la sección **"Environment Variables"**, agrega:

```env
# URL del backend API (usa la URL de Render del backend)
VITE_API_URL=https://ahorify-api.onrender.com

# Google OAuth (debe coincidir con el backend)
VITE_GOOGLE_CLIENT_ID=tu-google-client-id.apps.googleusercontent.com
```

### Paso 14: Verificar que el Frontend funciona

1. Render iniciará el build automáticamente
2. Espera a que termine (puede tardar 3-5 minutos)
3. Ve a la URL del frontend (ej: `https://ahorify-frontend.onrender.com`)
4. Deberías ver la aplicación funcionando

---

## 📋 PARTE 5: CONFIGURAR GOOGLE OAUTH

### Paso 15: Actualizar Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Ve a **APIs & Services > Credentials**
3. Edita tu **OAuth 2.0 Client ID**
4. Agrega a **Authorized JavaScript origins**:
   - `https://ahorify-frontend.onrender.com`
5. Agrega a **Authorized redirect URIs**:
   - `https://ahorify-frontend.onrender.com`
6. Guarda los cambios

### Paso 16: Actualizar Variables de Entorno

1. **Backend en Render**: Actualiza `ALLOWED_ORIGINS`:
   ```env
   ALLOWED_ORIGINS=https://ahorify-frontend.onrender.com
   ```
2. Render reiniciará automáticamente el servicio

---

## 📋 PARTE 6: VERIFICACIÓN FINAL

### Paso 17: Probar la aplicación

1. **Health Check del Backend**:
   ```bash
   curl https://ahorify-api.onrender.com/
   ```
   Debe responder con status "healthy"

2. **Frontend**:
   - Abre `https://ahorify-frontend.onrender.com`
   - Intenta hacer login con Google
   - Verifica que las peticiones al API funcionen

3. **Logs**:
   - En Render, ve a cada servicio
   - Click en **"Logs"** para ver los logs en tiempo real
   - Verifica que no haya errores

### Paso 18: Configurar Dominio Personalizado (Opcional)

Si tienes un dominio:

1. En Render, ve al servicio (backend o frontend)
2. Click en **"Settings"**
3. Scroll hasta **"Custom Domains"**
4. Agrega tu dominio
5. Configura los DNS según las instrucciones de Render

---

## 🐛 TROUBLESHOOTING

### Backend no inicia

- ✅ Verifica los logs en Render
- ✅ Verifica que `DATABASE_URL` sea correcta (Internal Database URL)
- ✅ Verifica que `gunicorn` esté en `requirements.txt`
- ✅ Verifica que el **Root Directory** sea `backend`
- ✅ Verifica que el **Start Command** use `$PORT` (variable de Render)

### Frontend no conecta con Backend

- ✅ Verifica que `VITE_API_URL` apunte a la URL correcta del backend
- ✅ Verifica CORS en el backend (`ALLOWED_ORIGINS`)
- ✅ Revisa la consola del navegador (F12) para errores CORS
- ✅ Verifica que el backend esté despierto (no en sleep)

### Base de datos no conecta

- ✅ Verifica que uses la **Internal Database URL** (no la externa)
- ✅ Verifica que la base de datos esté en la misma región
- ✅ Revisa los logs del backend para errores de conexión
- ✅ Verifica que la base de datos no esté en sleep

### Build falla

- ✅ Verifica que todas las dependencias estén en `requirements.txt` o `package.json`
- ✅ Revisa los logs de build en Render
- ✅ Verifica que el **Root Directory** sea correcto
- ✅ Para frontend, verifica que `node_modules` no esté en el repo

### Servicio se duerme (Free Plan)

- ⚠️ En el plan Free, los servicios se duermen después de 15 minutos de inactividad
- ⚠️ El primer request puede tardar 30-60 segundos (cold start)
- 💡 Para producción, considera el plan Starter ($7/mes) que no se duerme

---

## ✅ CHECKLIST FINAL

- [ ] Código subido a GitHub
- [ ] Base de datos PostgreSQL creada en Render
- [ ] Backend desplegado y funcionando
- [ ] Frontend desplegado y funcionando
- [ ] Variables de entorno configuradas correctamente
- [ ] Google OAuth configurado con URLs de producción
- [ ] Health check respondiendo
- [ ] Login con Google funcionando
- [ ] Logs sin errores críticos
- [ ] CORS configurado correctamente

---

## 📝 NOTAS IMPORTANTES

### Plan Free de Render

1. **Sleep Mode**:
   - Los servicios se "duermen" después de 15 minutos de inactividad
   - El primer request puede tardar 30-60 segundos (cold start)
   - Para producción, considera el plan Starter ($7/mes)

2. **Base de Datos**:
   - El plan Free tiene límites (90 días de retención)
   - Para producción, considera un plan pago

3. **Variables de Entorno**:
   - Nunca subas `.env` a GitHub
   - Usa siempre las variables de entorno de Render
   - Las variables se pueden actualizar sin redeploy

4. **Actualizaciones**:
   - Cada push a `main` desplegará automáticamente
   - Los cambios pueden tardar 2-5 minutos en aplicarse
   - Puedes ver el progreso en los logs

5. **URLs de Render**:
   - Backend: `https://ahorify-api.onrender.com`
   - Frontend: `https://ahorify-frontend.onrender.com`
   - Puedes cambiar el nombre en Settings > Name

---

## 🚀 PRÓXIMOS PASOS

1. **Monitoreo**: Configura alertas en Render para errores
2. **Backups**: Configura backups automáticos de la base de datos
3. **Dominio**: Configura un dominio personalizado
4. **SSL**: Render proporciona SSL automático (HTTPS)
5. **Escalado**: Considera planes superiores cuando crezcas

---

**¡Listo! Tu aplicación debería estar funcionando en Render.com 🚀**

Si encuentras problemas, revisa los logs en Render y la sección de Troubleshooting.

