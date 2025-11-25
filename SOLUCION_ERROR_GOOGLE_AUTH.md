# 🔧 Solución: Error de Google Authentication

## ❌ Error Principal
```
[GSI_LOGGER]: The given origin is not allowed for the given client ID.
Failed to load resource: the server responded with a status of 403
```

## 🔍 Causa
El Client ID de Google no tiene autorizado el origen `http://localhost:3000` en Google Cloud Console.

## ✅ Solución

### Paso 1: Ir a Google Cloud Console
1. Ve a: https://console.cloud.google.com/
2. Selecciona tu proyecto (o crea uno nuevo)
3. Ve a **APIs & Services** > **Credentials**

### Paso 2: Configurar Orígenes Autorizados
1. Busca tu **OAuth 2.0 Client ID** (el que termina en `.apps.googleusercontent.com`)
2. Haz clic en el nombre del Client ID para editarlo
3. En la sección **Authorized JavaScript origins**, agrega:
   ```
   http://localhost:3000
   http://localhost:5173
   ```
4. En la sección **Authorized redirect URIs**, agrega:
   ```
   http://localhost:3000
   http://localhost:5173
   ```
5. Haz clic en **Save**

### Paso 3: Verificar Configuración del Backend
Asegúrate de que el archivo `backend/.env` tenga:
```env
GOOGLE_CLIENT_ID=348454854956-dpd4cef270rhe2f50q1gmo3b4l2mhmav.apps.googleusercontent.com
```

### Paso 4: Reiniciar Servidores
Después de hacer los cambios en Google Cloud Console:
1. Espera 1-2 minutos para que los cambios se propaguen
2. Reinicia el frontend (Ctrl+C y vuelve a ejecutar `npm run dev`)
3. Limpia la caché del navegador (Ctrl+Shift+R o Cmd+Shift+R)

## 📝 Notas Importantes

- Los cambios en Google Cloud Console pueden tardar hasta 5 minutos en propagarse
- Asegúrate de que el Client ID en `.env` coincida exactamente con el de Google Cloud Console
- Para producción, también necesitarás agregar tu dominio (ej: `https://ahorify.com`)

## 🧪 Verificar que Funciona

1. Abre la consola del navegador (F12)
2. Deberías ver que el botón de Google se carga sin errores 403
3. Al hacer clic, deberías poder iniciar sesión correctamente

