# core/config_db.py
"""
Configuración de base de datos PostgreSQL
Para usar con Neon, Supabase u otros servicios de PostgreSQL en la nube
"""

import os
from typing import Optional

# Cargar variables de entorno desde archivo .env automáticamente
try:
    from dotenv import load_dotenv
    load_dotenv()  # Carga el archivo .env si existe
except ImportError:
    # Si python-dotenv no está instalado, simplemente no cargamos .env
    pass

# URL de conexión PostgreSQL
# Formato: postgresql://usuario:password@host:puerto/database
# Ejemplo para Neon: postgresql://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
DATABASE_URL: Optional[str] = os.getenv(
    "DATABASE_URL",
    None  # Debe ser configurado en variables de entorno
)

# Configuración alternativa (si prefieres variables separadas)
DB_HOST: Optional[str] = os.getenv("DB_HOST", None)
DB_PORT: Optional[str] = os.getenv("DB_PORT", "5432")
DB_NAME: Optional[str] = os.getenv("DB_NAME", None)
DB_USER: Optional[str] = os.getenv("DB_USER", None)
DB_PASSWORD: Optional[str] = os.getenv("DB_PASSWORD", None)

def get_database_url() -> str:
    """
    Obtiene la URL de conexión a PostgreSQL.
    Prioridad: DATABASE_URL > variables individuales
    """
    if DATABASE_URL:
        return DATABASE_URL
    
    if all([DB_HOST, DB_NAME, DB_USER, DB_PASSWORD]):
        return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    raise ValueError(
        "❌ DATABASE_URL no configurada. "
        "Configura la variable de entorno DATABASE_URL o las variables individuales (DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)"
    )

