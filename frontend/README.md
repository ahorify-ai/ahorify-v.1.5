# Ahorify Frontend

Frontend React + Vite + Tailwind para Ahorify V1.5

## 🚀 Instalación

```bash
cd frontend
npm install
```

## ⚙️ Configuración

1. Copia `.env.example` a `.env`:
```bash
cp .env.example .env
```

2. Edita `.env` y configura:
```env
VITE_API_URL=http://localhost:8000
VITE_GOOGLE_CLIENT_ID=tu-google-client-id.apps.googleusercontent.com
```

## 🏃 Ejecutar en desarrollo

```bash
npm run dev
```

La app estará disponible en: `http://localhost:3000`

## 📦 Build de producción

```bash
npm run build
```

Los archivos se generarán en `dist/`

## 🔌 Endpoints conectados

- ✅ `POST /api/v1/auth/google` - Autenticación Google
- ✅ `POST /api/v1/user/goal` - Guardar objetivo
- ✅ `POST /api/v1/gasto` - Registrar gasto
- ✅ `GET /api/v1/racha` - Obtener racha
- ✅ `GET /api/v1/gastos/recent` - Feed de gastos

## 📁 Estructura

```
frontend/
├── src/
│   ├── pages/          # Pantallas principales
│   │   ├── LoginScreen.jsx
│   │   ├── GoalScreen.jsx
│   │   └── Dashboard.jsx
│   ├── services/       # API client
│   │   └── api.js
│   ├── App.jsx         # Router principal
│   └── main.jsx        # Entry point
├── package.json
└── vite.config.js
```

