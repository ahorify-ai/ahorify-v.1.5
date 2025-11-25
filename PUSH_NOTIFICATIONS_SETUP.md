# 🔔 Configuración de Push Notifications - Ahorify

## ✅ Implementación Completada

Se ha implementado el sistema completo de push notifications usando OneSignal para PWA.

### Últimas mejoras:
- ✅ Icono de 180x180 agregado al manifest (compatibilidad iOS)
- ✅ Service Worker mejorado para mejor integración con OneSignal
- ✅ Componente opcional de gestión de notificaciones creado
- ✅ Integración completa OneSignal + PWA verificada

## 📋 Pasos de Configuración

### 1. Configurar OneSignal

1. Crear cuenta en https://onesignal.com
2. Crear nueva app: "Ahorify Web"
3. Seleccionar plataforma: **Web Push**
4. Configurar:
   - **Site URL**: `http://localhost:3000` (desarrollo) / `https://tu-dominio.com` (producción)
   - **Default Notification Icon**: usar `ahorify_icon.png`
5. Copiar credenciales:
   - **App ID**
   - **REST API Key**

### 2. Configurar Variables de Entorno

#### Backend (`backend/.env`):
```env
ONESIGNAL_APP_ID=tu-app-id-aqui
ONESIGNAL_REST_API_KEY=tu-rest-api-key-aqui
```

#### Frontend (`frontend/.env`):
```env
VITE_ONESIGNAL_APP_ID=tu-app-id-aqui
```

### 3. Instalar Dependencias

#### Frontend:
```bash
cd frontend
npm install
```

#### Backend:
```bash
cd backend
source venv_env/bin/activate
pip install -r requirements.txt
```

### 4. Migrar Base de Datos

La tabla `device_subscriptions` se creará automáticamente al iniciar el servidor FastAPI, o puedes ejecutar:

```python
from api.database import engine, Base
from api.models import DeviceSubscription

Base.metadata.create_all(bind=engine, tables=[DeviceSubscription.__table__])
```

### 5. Configurar Recordatorios Automáticos (Opcional)

#### Opción A: Usando Cron (Linux/Mac)

Agregar a crontab:
```bash
crontab -e
```

Agregar línea:
```bash
# Enviar recordatorios diarios a las 20:00
0 20 * * * cd /ruta/a/ahorify/backend && /ruta/a/venv/bin/python scripts/send_daily_reminders.py
```

#### Opción B: Usando APScheduler (Recomendado para producción)

1. Instalar APScheduler:
```bash
pip install apscheduler
```

2. El código ya está preparado en `backend/api/tasks.py` (crear si no existe)
3. Descomentar las líneas en `backend/api/main.py` para iniciar el scheduler

## 🧪 Testing

### 1. Verificar PWA
- Abrir DevTools → Application → Manifest
- Verificar que el manifest se carga correctamente
- Verificar Service Worker en Application → Service Workers

### 2. Verificar OneSignal
- Abrir DevTools → Console
- Deberías ver: `✅ OneSignal inicializado correctamente`
- Verificar Player ID en la consola

### 3. Probar Notificación Manual

Desde el backend, puedes probar enviando una notificación:

```python
from api.database import SessionLocal
from api.models import User, DeviceSubscription
from api.v1.services.notification_service import NotificationService

db = SessionLocal()
user = db.query(User).first()  # Obtener un usuario
NotificationService.send_streak_reminder(db, user)
```

## 📱 Funcionalidades Implementadas

### Frontend
- ✅ PWA configurado (manifest.json, service worker)
- ✅ OneSignal SDK integrado
- ✅ Solicitud automática de permisos
- ✅ Registro de dispositivos
- ✅ Suscripción/desuscripción

### Backend
- ✅ Modelo `DeviceSubscription` en base de datos
- ✅ Endpoints de suscripción/desuscripción
- ✅ Servicio de notificaciones con OneSignal
- ✅ Recordatorios de racha
- ✅ Alertas de racha en riesgo
- ✅ Notificaciones de hitos (milestones)

### Scripts
- ✅ Script de recordatorios diarios (`scripts/send_daily_reminders.py`)

## 🔧 Endpoints API

### POST `/api/v1/notifications/subscribe`
Registra un dispositivo para recibir notificaciones.

**Request:**
```json
{
  "google_id": "user_google_id",
  "player_id": "onesignal_player_id",
  "device_type": "web",
  "user_agent": "Mozilla/5.0..."
}
```

### POST `/api/v1/notifications/unsubscribe`
Desactiva las notificaciones para un dispositivo.

**Query params:**
- `player_id`: OneSignal Player ID
- `google_id`: Google ID del usuario

## 📝 Notas Importantes

1. **HTTPS requerido en producción**: OneSignal requiere HTTPS para funcionar en producción (excepto localhost).

2. **Permisos del navegador**: Los usuarios deben aceptar los permisos de notificaciones.

3. **Service Worker**: El service worker se registra automáticamente con VitePWA.

4. **Testing local**: OneSignal funciona en localhost sin HTTPS gracias a `allowLocalhostAsSecureOrigin: true`.

## 🚀 Próximos Pasos

- [ ] Configurar dominio en producción
- [ ] Configurar cron/APScheduler para recordatorios
- [x] Agregar UI para gestionar preferencias de notificaciones (componente creado)
- [ ] Implementar notificaciones de hitos (7 días, 30 días, etc.)
- [ ] Testing en dispositivos móviles reales

## 📦 Componente de Gestión de Notificaciones

Se ha creado un componente opcional `NotificationSettings.jsx` que puedes usar en tu Dashboard:

```jsx
import NotificationSettings from './components/NotificationSettings';

// En tu Dashboard o pantalla de configuración:
<NotificationSettings googleId={userData.googleId} />
```

Este componente permite a los usuarios:
- Ver el estado actual de las notificaciones
- Activar/desactivar notificaciones
- Gestionar permisos

