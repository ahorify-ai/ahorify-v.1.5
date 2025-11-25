# 🔍 Verificación Paso a Paso - Google Cloud Console

## ⚠️ El error 403 persiste - Verifica estos puntos:

### 1. **Tipo de Client ID** (MUY IMPORTANTE)
El Client ID debe ser de tipo **"Web application"**, NO "Desktop app" ni otro tipo.

**Cómo verificar:**
1. Ve a: https://console.cloud.google.com/apis/credentials
2. Haz clic en tu OAuth 2.0 Client ID
3. **VERIFICA** que en la parte superior diga: **"Application type: Web application"**
4. Si dice otro tipo, **CREA UNO NUEVO** de tipo "Web application"

### 2. **Orígenes Autorizados - Formato Exacto**
Los orígenes deben estar **EXACTAMENTE** así (sin espacios, sin trailing slash):

```
http://localhost:3000
```

**NO debe ser:**
- ❌ `http://localhost:3000/` (con trailing slash)
- ❌ `https://localhost:3000` (con https)
- ❌ `localhost:3000` (sin http://)
- ❌ `http://localhost:3000 ` (con espacio al final)

**Cómo verificar:**
1. En Google Cloud Console, ve a tu OAuth 2.0 Client ID
2. En "Authorized JavaScript origins", verifica que veas:
   ```
   http://localhost:3000
   ```
3. Si no está exactamente así, **ELIMÍNALO** y **AGREGA** de nuevo con el formato correcto
4. **GUARDA** los cambios

### 3. **URIs de Redireccionamiento**
En "Authorized redirect URIs", debe estar:
```
http://localhost:3000
```

### 4. **Guardar y Esperar**
1. Después de hacer cambios, **HAZ CLIC EN "GUARDAR"** (botón azul abajo)
2. Espera **5-10 minutos** para que Google propague los cambios
3. **Cierra TODAS las pestañas** de `localhost:3000`
4. **Limpia la caché del navegador** (Ctrl+Shift+Delete o Cmd+Shift+Delete)
5. Abre una **ventana de incógnito** y prueba de nuevo

### 5. **Verificar que el Client ID sea el Correcto**
El Client ID debe ser exactamente:
```
348454854956-dpd4cef270rhe2f50q1gmo3b4l2mhmav.apps.googleusercontent.com
```

Verifica que sea el mismo en:
- ✅ Google Cloud Console
- ✅ `frontend/.env` (VITE_GOOGLE_CLIENT_ID)
- ✅ `backend/.env` (GOOGLE_CLIENT_ID)

### 6. **Problema con Service Worker**
El Service Worker (Workbox) puede estar interceptando las peticiones. Para probar:

1. Abre DevTools (F12)
2. Ve a la pestaña **Application** (o **Aplicación**)
3. Ve a **Service Workers**
4. Haz clic en **Unregister** para desregistrar el service worker
5. Recarga la página (Ctrl+Shift+R o Cmd+Shift+R)

### 7. **Verificar en Modo Incógnito**
Prueba en una **ventana de incógnito** para evitar problemas de caché:
1. Abre una ventana de incógnito (Ctrl+Shift+N o Cmd+Shift+N)
2. Ve a `http://localhost:3000`
3. Intenta iniciar sesión

### 8. **Si Nada Funciona - Crear Nuevo Client ID**
Si después de todo esto sigue sin funcionar:

1. Ve a Google Cloud Console > Credentials
2. **CREA UN NUEVO** OAuth 2.0 Client ID:
   - Tipo: **Web application**
   - Nombre: "Ahorify Web Client"
   - Authorized JavaScript origins: `http://localhost:3000`
   - Authorized redirect URIs: `http://localhost:3000`
3. **COPIA** el nuevo Client ID
4. **ACTUALIZA** `frontend/.env` con el nuevo Client ID
5. **ACTUALIZA** `backend/.env` con el nuevo Client ID
6. **REINICIA** el frontend y backend
7. Prueba de nuevo

---

## 📸 Captura de Pantalla de Referencia

Tu configuración en Google Cloud Console debe verse así:

**Authorized JavaScript origins:**
```
http://localhost:3000
```

**Authorized redirect URIs:**
```
http://localhost:3000
```

**Application type:**
```
Web application
```

---

## ⏱️ Tiempo de Propagación
Los cambios en Google Cloud Console pueden tardar **5-15 minutos** en propagarse. Si acabas de hacer cambios, espera un poco antes de probar de nuevo.

