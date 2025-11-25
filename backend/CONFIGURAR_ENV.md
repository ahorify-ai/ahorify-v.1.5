# 🔧 Configuración del archivo .env

## Paso 1: Crear el archivo .env

En la raíz del proyecto (`/Users/tristansepulvedacebrian/Desktop/ahorify/backend/`), crea un archivo llamado `.env`:

```bash
cd /Users/tristansepulvedacebrian/Desktop/ahorify/backend
touch .env
```

O crea el archivo desde tu editor.

## Paso 2: Agregar variables de entorno

Edita el archivo `.env` y agrega las siguientes variables:

```env
# Base de datos
DATABASE_URL=postgresql://usuario:password@host:port/database

# Google OAuth (Feature 1)
GOOGLE_CLIENT_ID=tu-google-client-id.apps.googleusercontent.com

# Waitlist (Feature 2)
WAITLIST_LIMIT=50

# OneSignal Push Notifications (Feature 10)
ONESIGNAL_APP_ID=tu-onesignal-app-id
ONESIGNAL_REST_API_KEY=tu-onesignal-rest-api-key
```

### Ejemplo para Neon:
```env
DATABASE_URL=postgresql://neondb_owner:npg_xxxxxxxxx@ep-cool-darkness-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### Ejemplo para Supabase:
```env
DATABASE_URL=postgresql://postgres.xxxxxxxxx:tu_password@aws-0-eu-central-1.pooler.supabase.com:6543/postgres
```

### Ejemplo para PostgreSQL local:
```env
DATABASE_URL=postgresql://usuario:password@localhost:5432/ahorify
```

## Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

Esto instalará `python-dotenv` que carga automáticamente el archivo `.env`.

## Paso 4: Verificar

```bash
python test_postgres_connection.py
```

Deberías ver: `✅ ¡Conexión exitosa!`

---

## ✅ Listo

Una vez configurado el `.env`, el código cargará automáticamente la variable `DATABASE_URL` cada vez que ejecutes la aplicación.

**Nota:** El archivo `.env` ya está en `.gitignore`, así que no se subirá a Git (mantiene tus credenciales seguras).

