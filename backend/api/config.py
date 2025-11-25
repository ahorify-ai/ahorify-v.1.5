# api/config.py
"""
Configuración centralizada para FastAPI
Reutiliza la configuración de base de datos existente
"""

import os
from typing import Optional

# Cargar .env automáticamente
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Importar después de cargar .env
from core.config_db import get_database_url

# Database URL (reutiliza core/config_db.py)
DATABASE_URL = get_database_url()

# Waitlist Configuration
WAITLIST_LIMIT = int(os.getenv("WAITLIST_LIMIT", "50"))  # Feature 2: Escasez

# Beta Slots Configuration
# Nota: No hay límite real, todos pueden entrar. Este valor es solo para cálculo de urgencia en frontend
MAX_BETA_USERS = int(os.getenv("MAX_BETA_USERS", "10000"))  # Límite muy alto para cálculo de urgencia

# Environment Configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()

# API Configuration
API_V1_PREFIX = "/api/v1"
PROJECT_NAME = "Ahorify API"
VERSION = "1.5.0"

# CORS Configuration (configurable desde variables de entorno)
# Formato: "origin1,origin2,origin3" o lista separada por comas
_cors_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:5173"
)
ALLOWED_ORIGINS = [origin.strip() for origin in _cors_origins.split(",") if origin.strip()]

# En producción, agregar dominio de producción si no está en ALLOWED_ORIGINS
if ENVIRONMENT == "production":
    production_domain = os.getenv("PRODUCTION_DOMAIN")
    if production_domain and production_domain not in ALLOWED_ORIGINS:
        ALLOWED_ORIGINS.append(production_domain)

# OneSignal Configuration (Feature 10 - preparado)
ONESIGNAL_APP_ID = os.getenv("ONESIGNAL_APP_ID", None)
ONESIGNAL_REST_API_KEY = os.getenv("ONESIGNAL_REST_API_KEY", None)

# DeepSeek Configuration (Feature 5 - preparado)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", None)
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")

# Google OAuth Configuration (Feature 1 - ✅ Implementado)
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", None)  # Opcional para V1.5

