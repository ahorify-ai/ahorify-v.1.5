# api/database.py
"""
Configuración de SQLAlchemy para FastAPI
SessionLocal y engine para conexión a PostgreSQL
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from api.config import DATABASE_URL
import logging

logger = logging.getLogger(__name__)

# Engine de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verifica conexiones antes de usar
    pool_size=5,
    max_overflow=10,
    echo=False  # Cambiar a True para debug SQL
)

# SessionLocal para dependencias FastAPI
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos SQLAlchemy
Base = declarative_base()

def get_db():
    """
    Dependency para FastAPI - obtiene sesión de DB
    Usar con: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Inicializa las tablas en la base de datos"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tablas de base de datos creadas/verificadas")
    except Exception as e:
        logger.error(f"❌ Error creando tablas: {e}")
        raise

