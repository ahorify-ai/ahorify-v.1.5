# 🚀 Guía de Deploy - Ahorify V1.5

Esta guía te ayudará a desplegar Ahorify V1.5 en producción.

## 📋 Prerequisitos

- Servidor con Python 3.9+ y Node.js 18+
- Base de datos PostgreSQL (Neon, Supabase, o servidor propio)
- Dominio configurado (opcional pero recomendado)
- Cuenta de Google Cloud Console para OAuth

---

## 🔧 Configuración del Backend

### 1. Variables de Entorno

Crea un archivo `.env` en `backend/` basándote en `backend/.env.example`:

```bash
cd backend
cp .env.example .env
nano .env  # o tu editor preferido
```

**Variables requeridas:**

```env
# Entorno
ENVIRONMENT=production

# Base de datos PostgreSQL
DATABASE_URL=postgresql://usuario:password@host:port/database

# Google OAuth
GOOGLE_CLIENT_ID=tu-google-client-id.apps.googleusercontent.com

# CORS - Agrega tu dominio de producción
ALLOWED_ORIGINS=https://ahorify.com,https://www.ahorify.com
PRODUCTION_DOMAIN=https://ahorify.com

# Waitlist
WAITLIST_LIMIT=50
```

**Variables opcionales:**

```env
# OneSignal (si usas notificaciones push)
ONESIGNAL_APP_ID=tu-app-id
ONESIGNAL_REST_API_KEY=tu-api-key

# DeepSeek (si usas parsing inteligente)
DEEPSEEK_API_KEY=tu-api-key
```

### 2. Instalar Dependencias

```bash
cd backend
python3 -m venv venv_env
source venv_env/bin/activate  # En Windows: venv_env\Scripts\activate
pip install -r requirements.txt
```

### 3. Verificar Conexión a Base de Datos

```bash
python test_postgres_connection.py
```

Deberías ver: `✅ ¡Conexión exitosa!`

### 4. Ejecutar Backend

**Desarrollo:**
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Producción (con Gunicorn recomendado):**
```bash
pip install gunicorn
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**O con systemd (recomendado para producción):**

Crea `/etc/systemd/system/ahorify-api.service`:

```ini
[Unit]
Description=Ahorify API
After=network.target

[Service]
User=tu-usuario
WorkingDirectory=/ruta/a/ahorify/backend
Environment="PATH=/ruta/a/ahorify/backend/venv_env/bin"
ExecStart=/ruta/a/ahorify/backend/venv_env/bin/gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Activar servicio:
```bash
sudo systemctl enable ahorify-api
sudo systemctl start ahorify-api
sudo systemctl status ahorify-api
```

---

## 🎨 Configuración del Frontend

### 1. Variables de Entorno

Crea un archivo `.env` en `frontend/` basándote en `frontend/.env.example`:

```bash
cd frontend
cp .env.example .env
nano .env
```

**Variables requeridas:**

```env
# URL del backend API
VITE_API_URL=https://api.ahorify.com

# Google OAuth (debe coincidir con el backend)
VITE_GOOGLE_CLIENT_ID=tu-google-client-id.apps.googleusercontent.com
```

### 2. Instalar Dependencias

```bash
cd frontend
npm install
```

### 3. Build para Producción

```bash
npm run build
```

Esto generará la carpeta `dist/` con los archivos estáticos listos para servir.

### 4. Servir Frontend

**Opción 1: Nginx (Recomendado)**

Configuración de ejemplo `/etc/nginx/sites-available/ahorify`:

```nginx
server {
    listen 80;
    server_name ahorify.com www.ahorify.com;

    # Redirigir a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ahorify.com www.ahorify.com;

    ssl_certificate /ruta/a/certificado.crt;
    ssl_certificate_key /ruta/a/llave.key;

    root /ruta/a/ahorify/frontend/dist;
    index index.html;

    # SPA - Redirigir todas las rutas a index.html
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache para assets estáticos
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Proxy para API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Activar configuración:
```bash
sudo ln -s /etc/nginx/sites-available/ahorify /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

**Opción 2: Servir con Vite Preview (solo para pruebas)**

```bash
npm run preview
```

**Opción 3: Servir con servidor estático simple**

```bash
# Con Python
cd dist
python3 -m http.server 3000

# Con Node.js (http-server)
npm install -g http-server
http-server dist -p 3000
```

---

## 🔐 Configuración de Google OAuth

### 1. Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Ve a **APIs & Services > Credentials**
4. Crea **OAuth 2.0 Client ID**
5. Configura:
   - **Application type**: Web application
   - **Authorized JavaScript origins**: 
     - `http://localhost:3000` (desarrollo)
     - `https://ahorify.com` (producción)
   - **Authorized redirect URIs**:
     - `http://localhost:3000` (desarrollo)
     - `https://ahorify.com` (producción)

### 2. Actualizar Variables de Entorno

Copia el **Client ID** y actualiza:
- `backend/.env`: `GOOGLE_CLIENT_ID`
- `frontend/.env`: `VITE_GOOGLE_CLIENT_ID`

---

## 🗄️ Base de Datos

### Opciones Recomendadas

1. **Neon** (PostgreSQL serverless)
   - https://neon.tech
   - Gratis hasta cierto límite
   - Fácil de configurar

2. **Supabase**
   - https://supabase.com
   - PostgreSQL + extras
   - Plan gratuito disponible

3. **Railway / Render**
   - PostgreSQL gestionado
   - Fácil deploy

### Migración de Datos

Las tablas se crean automáticamente al iniciar la aplicación gracias a SQLAlchemy:

```python
Base.metadata.create_all(bind=engine)
```

Si necesitas migraciones más complejas, considera usar **Alembic**.

---

## 🔒 Seguridad

### Checklist de Seguridad

- [ ] Variables de entorno configuradas (nunca en el código)
- [ ] HTTPS habilitado (certificado SSL)
- [ ] CORS configurado correctamente (solo dominios permitidos)
- [ ] Base de datos con conexión segura (SSL)
- [ ] Secrets fuera del repositorio (`.env` en `.gitignore`)
- [ ] Logs no exponen información sensible
- [ ] Rate limiting configurado (considera usar `slowapi`)
- [ ] Firewall configurado (solo puertos necesarios abiertos)

### Agregar Rate Limiting (Opcional)

```bash
pip install slowapi
```

En `backend/api/main.py`:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

---

## 📊 Monitoreo y Logs

### Ver Logs del Backend

```bash
# Si usas systemd
sudo journalctl -u ahorify-api -f

# Si usas Gunicorn directamente
# Los logs aparecerán en stdout/stderr
```

### Health Check

Verifica que la API esté funcionando:

```bash
curl https://api.ahorify.com/
```

Deberías recibir:
```json
{
  "status": "healthy",
  "database": "✅ Connected",
  "version": "1.5.0",
  "timestamp": "..."
}
```

---

## 🚀 Deploy Continuo (CI/CD)

### GitHub Actions (Ejemplo)

Crea `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /ruta/a/ahorify/backend
            git pull
            source venv_env/bin/activate
            pip install -r requirements.txt
            sudo systemctl restart ahorify-api

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      - name: Build
        run: |
          cd frontend
          npm install
          npm run build
      - name: Deploy
        uses: appleboy/scp-action@master
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          source: "frontend/dist/*"
          target: "/ruta/a/ahorify/frontend/dist"
```

---

## 🐛 Troubleshooting

### Backend no inicia

1. Verifica variables de entorno: `echo $DATABASE_URL`
2. Verifica conexión a DB: `python test_postgres_connection.py`
3. Revisa logs: `sudo journalctl -u ahorify-api -n 50`

### Frontend no conecta con Backend

1. Verifica `VITE_API_URL` en `.env`
2. Verifica CORS en backend (`ALLOWED_ORIGINS`)
3. Verifica que el proxy de Nginx esté configurado correctamente

### Google OAuth no funciona

1. Verifica que el dominio esté en **Authorized JavaScript origins**
2. Verifica que `GOOGLE_CLIENT_ID` coincida en backend y frontend
3. Revisa la consola del navegador para errores

### Base de datos no conecta

1. Verifica `DATABASE_URL` (formato correcto)
2. Verifica que la IP del servidor esté permitida en el firewall de la DB
3. Verifica credenciales

---

## ✅ Checklist Final

Antes de considerar el deploy completo:

- [ ] Backend funcionando y accesible
- [ ] Frontend build exitoso
- [ ] Variables de entorno configuradas
- [ ] Google OAuth funcionando
- [ ] Base de datos conectada
- [ ] HTTPS configurado
- [ ] CORS configurado correctamente
- [ ] Health check respondiendo
- [ ] Logs funcionando
- [ ] Dominio apuntando correctamente

---

## 📚 Recursos Adicionales

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vite Production Build](https://vitejs.dev/guide/build.html)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [Google OAuth Setup](https://developers.google.com/identity/protocols/oauth2)

---

## 🆘 Soporte

Si encuentras problemas durante el deploy, revisa:
- Logs del backend
- Logs de Nginx: `sudo tail -f /var/log/nginx/error.log`
- Consola del navegador (F12)
- Health check endpoint

---

**¡Buena suerte con tu deploy! 🚀**

