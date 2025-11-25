# api/main.py
"""
FastAPI Main Application - Ahorify V1.5
Backend Mobile-First para PWA
"""

from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import logging

from api.config import (
    PROJECT_NAME, VERSION, ALLOWED_ORIGINS,
    WAITLIST_LIMIT, GOOGLE_CLIENT_ID, ENVIRONMENT
)
from api.database import get_db, engine
from api.models import User, DeviceSubscription  # Importar todos los modelos para que SQLAlchemy los registre
from api.schemas import HealthCheckResponse
from api.v1.endpoints import router as v1_router

# Configurar logging según entorno
log_level = logging.DEBUG if ENVIRONMENT == "development" else logging.INFO
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    description="Backend API para Ahorify V1.5 - PWA Mobile-First",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ==================== CORS Configuration ====================
# Feature: Permitir React frontend (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Inicialización ====================
@app.on_event("startup")
async def startup_event():
    """Inicializa la base de datos al arrancar"""
    try:
        # Inicializar tablas SQLAlchemy
        from api.database import Base
        Base.metadata.create_all(bind=engine)
        logger.info("✅ FastAPI iniciado correctamente")
        logger.info(f"📊 Waitlist limit: {WAITLIST_LIMIT} usuarios")
        logger.info(f"🌍 Entorno: {ENVIRONMENT}")
        
        # Verificar configuración Google Auth
        if GOOGLE_CLIENT_ID:
            logger.info(f"🔐 Google Auth: Configurado (Client ID: {GOOGLE_CLIENT_ID[:20]}...)")
        else:
            logger.warning("⚠️ Google Auth: GOOGLE_CLIENT_ID no configurado (modo desarrollo)")
        
        # Logs de URLs solo en desarrollo
        if ENVIRONMENT == "development":
            logger.info(f"🌐 API disponible en: http://localhost:8000")
            logger.info(f"📚 Docs disponibles en: http://localhost:8000/docs")
        else:
            logger.info(f"🌐 API iniciada en modo producción")
            logger.info(f"📚 Docs disponibles en: /docs")
    except Exception as e:
        logger.error(f"❌ Error iniciando FastAPI: {e}")

# ==================== Health Check ====================
@app.get("/", response_model=HealthCheckResponse)
def health_check(db: Session = Depends(get_db)):
    """
    Health check del API
    Verifica conexión a base de datos
    """
    try:
        # Verificar conexión a DB (SQLAlchemy 2.0 requiere text())
        db.execute(text("SELECT 1"))
        db_status = "✅ Connected"
    except Exception as e:
        db_status = f"❌ Error: {str(e)}"
    
    return HealthCheckResponse(
        status="healthy",
        database=db_status,
        version=VERSION,
        timestamp=datetime.now()
    )

# ==================== Incluir routers ====================
app.include_router(v1_router)

# ==================== Error Handlers ====================
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Endpoint no encontrado"}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    logger.error(f"Error interno: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )

# ==================== Main ====================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=(ENVIRONMENT == "development")  # Auto-reload solo en desarrollo
    )

