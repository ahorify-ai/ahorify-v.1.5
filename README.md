# 🚀 Ahorify V1.5

PWA Mobile-First para gestión de finanzas personales con gamificación estilo Duolingo.

## 📁 Estructura del Proyecto

```
ahorify/
├── backend/          # Backend FastAPI + PostgreSQL
└── frontend/         # Frontend React + Vite + Tailwind
```

## 🚀 Inicio Rápido

### Backend

```bash
cd backend
source venv_env/bin/activate
uvicorn api.main:app --reload
```

Backend disponible en: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend disponible en: `http://localhost:3000`

## ⚙️ Configuración

### Backend

1. Copia el archivo de ejemplo y configura tus variables:
```bash
cd backend
cp .env.example .env
# Edita .env con tus valores
```

2. Ver más detalles en `backend/CONFIGURAR_ENV.md`

### Frontend

1. Copia el archivo de ejemplo y configura tus variables:
```bash
cd frontend
cp .env.example .env
# Edita .env con tus valores
```

## 📚 Documentación

- **Deploy a Producción**: `DEPLOY.md` ⭐
- **Integración Frontend**: `INTEGRACION_FRONTEND.md`
- **Backend API**: `backend/api/README.md`
- **Configuración**: `backend/CONFIGURAR_ENV.md`
- **Arquitectura**: `backend/structure.py`

## 🎯 Features Implementadas

- ✅ Google Auth OAuth
- ✅ Waitlist Logic
- ✅ User Goal (Onboarding)
- ✅ Smart Text Input
- ✅ Aury Parser (básico)
- ✅ Dashboard Racha
- ✅ Feed con Roast
- ✅ Streak Freeze (Protector semanal)

## 🛠️ Stack Tecnológico

- **Backend**: FastAPI + PostgreSQL (Neon) + SQLAlchemy
- **Frontend**: React + Vite + Tailwind CSS
- **Auth**: Google OAuth 2.0

## 📝 Licencia

Proyecto privado - Ahorify V1.5

