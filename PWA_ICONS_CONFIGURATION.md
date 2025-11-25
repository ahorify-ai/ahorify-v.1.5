# 🎨 Configuración de Iconos PWA - Ahorify

## ✅ Iconos Generados

Todos los iconos han sido generados desde `backend/static/ahorify_logo.png` (1024x1024px) y están ubicados en `frontend/public/`:

### Favicons (Pestaña del navegador)
- `favicon.ico` - Multi-resolución (16x16, 32x32, 48x48)
- `favicon-16x16.png` - 16x16px
- `favicon-32x32.png` - 32x32px
- `favicon-48x48.png` - 48x48px

### Apple Touch Icon (iOS)
- `apple-touch-icon.png` - 180x180px (para "Añadir a pantalla de inicio" en iOS)

### PWA Icons (Manifest)
- `icon-192x192.png` - 192x192px (mínimo Android)
- `icon-512x512.png` - 512x512px (recomendado, splash screen)
- `icon-maskable-512x512.png` - 512x512px con padding seguro (Android adaptativo)

### Windows Tile (Opcional)
- `mstile-310x310.png` - 310x310px (para Windows)

## 📝 Archivos Configurados

### `frontend/index.html`
- ✅ Favicons configurados
- ✅ Apple Touch Icon configurado
- ✅ Meta tags para iOS
- ✅ Meta tags para Windows Tile
- ✅ Manifest link (generado automáticamente por VitePWA)

### `frontend/vite.config.js`
- ✅ VitePWA configurado con todos los iconos
- ✅ Manifest completo con:
  - Icons (192x192, 512x512, maskable)
  - Shortcuts (acceso rápido a "Registrar Gasto")
  - Categories (finance, productivity, lifestyle)
- ✅ Workbox configurado con estrategias de caché
- ✅ Runtime caching para Google Auth y API

### `frontend/src/main.jsx`
- ✅ Service Worker registration preparado

## 🔧 Cómo se Generaron

Se utilizó un script Python (`generate_icons.py`) con PIL/Pillow que:
1. Lee `backend/static/ahorify_logo.png` (1024x1024px)
2. Genera todas las versiones en los tamaños necesarios
3. Crea el favicon.ico multi-resolución
4. Genera el maskable icon con padding seguro (80% del tamaño)

## 📱 Uso en Diferentes Plataformas

### Chrome/Edge (Desktop y Android)
- Usa `icon-192x192.png` y `icon-512x512.png` del manifest
- Favicon en la pestaña: `favicon.ico`

### Safari (iOS)
- Apple Touch Icon: `apple-touch-icon.png` (180x180px)
- Se muestra cuando el usuario hace "Añadir a pantalla de inicio"

### Android
- Usa `icon-192x192.png` para la pantalla de inicio
- `icon-maskable-512x512.png` para iconos adaptativos (se adapta a diferentes formas)

### Windows
- Tile: `mstile-310x310.png`
- Color: #10b981 (verde Ahorify)

## 🚀 Próximos Pasos

1. **Testing**: Probar instalación en diferentes dispositivos
2. **Lighthouse**: Ejecutar audit PWA para validar
3. **Actualización**: Si cambias el logo, ejecutar `python3 generate_icons.py` de nuevo

## 📦 Archivos Generados

Todos los iconos están en `frontend/public/` y se incluyen automáticamente en el build de producción.

