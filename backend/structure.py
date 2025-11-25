"""
AHORIFY V1.5 - ARQUITECTURA DEL PROYECTO
========================================
Estado: PIVOT COMPLETADO ✅
De: MVP Streamlit (Desktop) → PWA Mobile-First (Gen-Z)
Backend: SQLite → PostgreSQL (Neon) + FastAPI
Frontend: Streamlit → React/Tailwind ✅ COMPLETADO

Última actualización: Enero 2025
"""

STRUCTURE = """
ahorify/
│
├── 🔥 BACKEND (FastAPI - V1.5)
│   ├── run_api.py                       # Script para ejecutar FastAPI
│   ├── test_fastapi.py                  # Tests de API
│   ├── test_postgres_connection.py      # Verificación conexión PostgreSQL
│   ├── requirements.txt                 # Dependencias Python
│   ├── .env                             # Variables de entorno (DATABASE_URL, etc.)
│   │
│   ├── api/                             # Backend FastAPI
│       ├── __init__.py
│       ├── main.py                      # FastAPI app principal + CORS + Health check
│       ├── config.py                    # Config centralizada (Waitlist, DeepSeek, OneSignal)
│       ├── database.py                  # SQLAlchemy + SessionLocal + Engine
│       ├── models.py                    # Modelos SQLAlchemy (User, Transaction, Streak)
│       ├── schemas.py                   # Schemas Pydantic (Request/Response)
│       ├── README.md                    # Documentación API
│       └── v1/
│           ├── __init__.py
│           ├── endpoints.py             # TODOS los endpoints API (7/10 features)
│           └── services/
│               ├── __init__.py
│               ├── aury_service.py      # Feature 5, 7: Parsing Smart Input + Aury responses
│               └── streak_service.py    # Feature 8: Lógica racha resiliente + Freeze
│   │
│   └── core/                            # Core business logic
│       ├── config_db.py                 # ✅ Config PostgreSQL (usado por FastAPI)
│       └── config_db.py                 # ✅ Config PostgreSQL (usado por FastAPI)
│       └── config_db.py                 # ✅ Config PostgreSQL (usado por FastAPI)
│
├── 🎨 FRONTEND (React + Vite + Tailwind)
│   ├── src/
│   │   ├── pages/                       # Pantallas principales
│   │   │   ├── LoginScreen.jsx          # Login con Google Auth
│   │   │   ├── GoalScreen.jsx           # Onboarding - establecer objetivo
│   │   │   └── Dashboard.jsx            # Dashboard principal
│   │   ├── services/
│   │   │   └── api.js                   # API client para FastAPI
│   │   ├── App.jsx                      # Router principal
│   │   └── main.jsx                     # Entry point
│   ├── package.json                     # Dependencias Node.js
│   ├── vite.config.js                   # Configuración Vite
│   └── tailwind.config.js               # Configuración Tailwind
│
├── 📁 DATOS (Backend)
│   └── data/
│       └── *.db                         # SQLite backups (legacy)
│
├── 🖼️ STATIC FILES (Backend)
│   └── static/
│       ├── ahorify_icon.png
│       ├── ahorify_logo.ico
│       └── ahorify_logo.png
│
└── 📚 DOCUMENTACIÓN
    ├── INTEGRACION_FRONTEND.md          # Guía integración frontend
    └── backend/
        ├── MIGRACION_POSTGRES.md        # Guía migración SQLite → PostgreSQL
        ├── MIGRACION_COMPLETADA.md      # Resumen migración
        ├── CONFIGURAR_ENV.md            # Setup variables de entorno
        └── api/README.md                # Documentación FastAPI
"""

# ==================== FEATURES IMPLEMENTADAS ====================
FEATURES_STATUS = """
✅ FEATURES COMPLETADAS (8/10):

✅ Feature 1: Google Auth OAuth
   - Endpoint: POST /api/v1/auth/google
   - Validación de tokens Google
   - Usa google_id como identificador principal
   - Crea/obtiene usuario automáticamente

✅ Feature 2: Waitlist Logic
   - Endpoint: GET /api/v1/waitlist/status
   - Cuenta usuarios totales vs límite configurable

✅ Feature 3: User Goal
   - Endpoint: POST /api/v1/user/goal
   - Guarda objetivo del usuario (compromiso)

✅ Feature 4: Smart Text Input
   - Endpoint: POST /api/v1/gasto
   - Recibe texto libre: "Pizza 15 euros"

✅ Feature 5: Aury Parser (Básico)
   - Parsing con regex (preparado para DeepSeek)
   - Extrae: amount, category, type

✅ Feature 6: Dashboard Racha Centrado
   - Endpoint: GET /api/v1/racha
   - Retorna: current_streak, longest_streak, freeze_inventory

✅ Feature 7: Feed con Roast
   - Endpoint: GET /api/v1/gastos/recent
   - Incluye aury_response (comentarios sarcásticos)

✅ Feature 8: Streak Freeze
   - Endpoint: POST /api/v1/streak/freeze
   - Lógica de vidas extra implementada

✅ Feature 9: Freemium Model
   - Campo is_plus_user en User
   - Campo streak_freezes_available
   - Endpoint: GET /api/v1/user/subscription

🚧 PENDIENTES (2/10):

🔄 Feature 5: DeepSeek Integration
   - Estructura lista en aury_service.py
   - Falta integrar API DeepSeek para parsing inteligente

🔄 Feature 10: Notificaciones OneSignal
   - Config preparado en api/config.py
   - Falta implementar cron + lógica de envío
"""

# ==================== BASE DE DATOS ====================
DATABASE_INFO = """
📊 BASE DE DATOS: PostgreSQL (Neon Cloud)

Tablas creadas automáticamente por SQLAlchemy:

1. users
   - id (UUID, PK)
   - email (VARCHAR, nullable)
   - goal (TEXT, nullable) ← Feature 3
   - is_plus_user (BOOLEAN) ← Feature 9
   - streak_freezes_available (INTEGER) ← Feature 8, 9
   - created_at, updated_at

2. transactions
   - id (UUID, PK)
   - user_id (FK → users)
   - raw_text (TEXT) ← Feature 4
   - amount (NUMERIC) ← Feature 5
   - category (VARCHAR) ← Feature 5
   - type (VARCHAR) ← Feature 5
   - aury_response (TEXT) ← Feature 7
   - created_at

3. streaks
   - user_id (UUID, PK, FK → users)
   - current_streak (INTEGER) ← Feature 6, 8
   - longest_streak (INTEGER)
   - last_activity_date (DATE)
   - created_at, updated_at

Migración:
✅ SQLite → PostgreSQL COMPLETADA
✅ Tablas adaptadas a PostgreSQL
✅ Queries migradas (?, ?) → (%s, %s)
✅ Constraints y tipos de datos actualizados
"""

# ==================== ENDPOINTS API ====================
API_ENDPOINTS = """
🔌 FASTAPI ENDPOINTS (http://localhost:8000)

BASE: /api/v1

✅ POST   /gasto                  # Feature 4, 5, 7: Smart Input + Aury
✅ GET    /gastos/recent          # Feature 7: Feed con Roast
✅ GET    /racha                  # Feature 6, 8: Dashboard Racha
✅ POST   /streak/freeze          # Feature 8: Usar vida extra
✅ GET    /waitlist/status        # Feature 2: Escasez
✅ POST   /user/goal              # Feature 3: Compromiso
✅ GET    /user/subscription      # Feature 9: Freemium (V2.0 - comentado)
✅ POST   /auth/google            # Feature 1: Google OAuth ✅ COMPLETADO

DOCS:
📚 Swagger UI: http://localhost:8000/docs
📚 ReDoc: http://localhost:8000/redoc
🔍 Health: http://localhost:8000/
"""

# ==================== ARQUITECTURA ====================
ARCHITECTURE = """
🏗️ ARQUITECTURA V1.5

┌─────────────────────────────────────────────────┐
│              FRONTEND (Futuro)                  │
│         React + Tailwind + PWA                  │
│         (Puerto 3000 / 5173)                    │
└──────────────────┬──────────────────────────────┘
                   │ HTTP/REST
                   ▼
┌─────────────────────────────────────────────────┐
│           FASTAPI BACKEND (Nuevo)               │
│  ┌─────────────────────────────────────────┐   │
│  │  api/v1/endpoints.py                    │   │
│  │  - Smart Input (Feature 4)              │   │
│  │  - Aury Parser (Feature 5)              │   │
│  │  - Racha Logic (Feature 6, 8)           │   │
│  │  - Feed con Roast (Feature 7)           │   │
│  └──────────────┬──────────────────────────┘   │
│                 │                                │
│  ┌──────────────▼──────────────────────────┐   │
│  │  api/v1/services/                       │   │
│  │  - aury_service.py                      │   │
│  │  - streak_service.py                    │   │
│  └──────────────┬──────────────────────────┘   │
└─────────────────┼──────────────────────────────┘
                  │ SQLAlchemy ORM
                  ▼
┌─────────────────────────────────────────────────┐
│      POSTGRESQL (Neon Cloud)                    │
│  - users                                        │
│  - transactions                                 │
│  - streaks                                      │
└─────────────────────────────────────────────────┘
"""

# ==================== PRÓXIMOS PASOS ====================
NEXT_STEPS = """
🚀 ROADMAP PRÓXIMOS PASOS:

1. ✅ COMPLETADO: Migración PostgreSQL
2. ✅ COMPLETADO: Setup FastAPI
3. ✅ COMPLETADO: Implementar Google Auth (Feature 1)
4. ✅ COMPLETADO: Frontend React/Tailwind
5. 🔄 PENDIENTE: Integrar DeepSeek API (Feature 5) - Mejora opcional
6. 🔄 PENDIENTE: Setup OneSignal Notificaciones (Feature 10)
7. 🔄 PENDIENTE: PWA Configuration
8. 🔄 PENDIENTE: Deploy a producción
9. 🔄 PENDIENTE: Dominio personalizado (ahorify.com)
"""

if __name__ == "__main__":
    print("=" * 70)
    print("AHORIFY V1.5 - ARQUITECTURA DEL PROYECTO")
    print("=" * 70)
    print(STRUCTURE)
    print("\n" + "=" * 70)
    print("FEATURES STATUS")
    print("=" * 70)
    print(FEATURES_STATUS)
    print("\n" + "=" * 70)
    print("BASE DE DATOS")
    print("=" * 70)
    print(DATABASE_INFO)
    print("\n" + "=" * 70)
    print("ENDPOINTS API")
    print("=" * 70)
    print(API_ENDPOINTS)
    print("\n" + "=" * 70)
    print("ARQUITECTURA")
    print("=" * 70)
    print(ARCHITECTURE)
    print("\n" + "=" * 70)
    print("PRÓXIMOS PASOS")
    print("=" * 70)
    print(NEXT_STEPS)
    print("=" * 70)
