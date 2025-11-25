# 🔍 Verificación de Google Cloud Console

## Pasos para verificar que está configurado correctamente:

### 1. Verificar que guardaste los cambios
- Ve a: https://console.cloud.google.com/apis/credentials
- Selecciona tu OAuth 2.0 Client ID
- **VERIFICA** que veas `http://localhost:3000` en ambas secciones:
  - ✅ "Orígenes autorizados de JavaScript"
  - ✅ "URIs de redireccionamiento autorizados"
- Si NO los ves, agrégalos y **GUARDA** de nuevo

### 2. Verificar el Client ID
- El Client ID debe ser exactamente: `348454854956-dpd4cef270rhe2f50q1gmo3b4l2mhmav.apps.googleusercontent.com`
- Verifica que sea el mismo en:
  - Google Cloud Console
  - `frontend/.env` (VITE_GOOGLE_CLIENT_ID)
  - `backend/.env` (GOOGLE_CLIENT_ID)

### 3. Limpiar caché del navegador
Después de guardar en Google Cloud Console:
1. **Cierra TODAS las pestañas** de `localhost:3000`
2. Abre una **ventana de incógnito** (Ctrl+Shift+N o Cmd+Shift+N)
3. Ve a: `http://localhost:3000`
4. Abre la consola (F12) y revisa los mensajes de debug

### 4. Verificar en la consola
Deberías ver estos mensajes:
```
🔍 Debug Google Sign-In:
  - Client ID: 348454854956-dpd4cef...
  - Current Origin: http://localhost:3000
  - Expected Origins: http://localhost:3000, http://localhost:5173
✅ Google Sign-In SDK cargado
✅ Inicializando Google Sign-In...
✅ Renderizando botón de Google...
✅ Botón de Google renderizado
```

### 5. Si sigue el error 403:
- **Espera 5-10 minutos** después de guardar (Google puede tardar)
- Verifica que el origen sea exactamente `http://localhost:3000` (sin `/` al final)
- Verifica que no haya espacios extra
- Intenta agregar también `http://127.0.0.1:3000` como origen alternativo

### 6. Verificar que el proyecto de Google Cloud esté activo
- Ve a: https://console.cloud.google.com/apis/dashboard
- Verifica que tu proyecto esté seleccionado
- Verifica que "Google Sign-In API" esté habilitada

## ⚠️ Problemas comunes:

1. **No guardaste los cambios**: Debes hacer clic en "Guardar" después de agregar los orígenes
2. **Cambios no propagados**: Google puede tardar hasta 10 minutos en propagar cambios
3. **Caché del navegador**: Usa ventana de incógnito para evitar caché
4. **Client ID incorrecto**: Verifica que sea el mismo en todos lados
5. **Origen con barra final**: No uses `http://localhost:3000/` (sin la barra final)

