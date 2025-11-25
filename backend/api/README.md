# 🚀 Ahorify API V1.5 - FastAPI Backend

Backend Mobile-First para PWA Ahorify. Arquitectura diseñada para las **10 features core** del pivot.

## 📋 Estructura

```
api/
├── main.py              # FastAPI app principal
├── config.py            # Configuración centralizada
├── database.py          # SQLAlchemy setup
├── models.py            # Modelos SQLAlchemy (User, Transaction, Streak)
├── schemas.py           # Schemas Pydantic (Request/Response)
└── v1/
    ├── endpoints.py     # Todas las rutas API
    └── services/
        ├── auth_service.py    # Feature 1: Google OAuth
        ├── aury_service.py    # Feature 5, 7: Parsing + Aury
        └── streak_service.py  # Feature 8: Lógica racha
```

## 🚀 Ejecutar la API

### Opción 1: Script directo
```bash
python run_api.py
```

### Opción 2: Uvicorn directo
```bash
uvicorn api.main:app --reload
```

La API estará disponible en: `http://localhost:8000`

## 📚 Documentación

Una vez corriendo, accede a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/

## 🔌 Endpoints Principales

### Feature 1: Google Auth ✅
```
POST /api/v1/auth/google
Body: {"token": "google_id_token"}
Response: {"google_id": "...", "email": "...", "is_new_user": true/false}
```

### Feature 4, 5, 7: Smart Input + Aury
```
POST /api/v1/gasto
Body: {"raw_text": "Pizza 15 euros", "google_id": "..."}
```

### Feature 6, 8: Racha
```
GET /api/v1/racha?google_id=...
```

### Feature 7: Feed con Roast
```
GET /api/v1/gastos/recent?google_id=...&limit=20
```

### Feature 2: Waitlist
```
GET /api/v1/waitlist/status
```

### Feature 8: Streak Freeze
```
POST /api/v1/streak/freeze
Body: {"google_id": "..."}
```

### Feature 3: User Goal
```
POST /api/v1/user/goal?google_id=...
Body: {"goal": "Viajar a Japón"}
```

## ✅ Pruebas

```bash
python test_fastapi.py
```

## 🔧 Configuración

Las variables de entorno se cargan desde `.env`:

```env
DATABASE_URL=postgresql://...
WAITLIST_LIMIT=50
GOOGLE_CLIENT_ID=...  # Feature 1: Google OAuth (requerido)
GOOGLE_CLIENT_SECRET=...  # Feature 1: Google OAuth (opcional)
DEEPSEEK_API_KEY=...  # Feature 5: Parsing inteligente (opcional)
ONESIGNAL_APP_ID=...  # Feature 10: Notificaciones (futuro)
```

## 📝 Notas

- Las tablas se crean automáticamente al iniciar
- CORS configurado para `localhost:3000` y `localhost:5173` (React/Vite)
- ✅ **Google Auth implementado** - Usa Google ID como identificador principal
- Todos los endpoints usan `google_id` en lugar de `user_id` (UUID)
- Modo desarrollo: Si `GOOGLE_CLIENT_ID` no está configurado, decodifica tokens sin verificar (requiere PyJWT)

