#!/usr/bin/env python3
"""
Script para cambiar user_id de VARCHAR a UUID eliminando el default primero
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.database import engine
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Ejecuta la migración"""
    logger.info("🚀 Cambiando user_id de VARCHAR a UUID...")
    
    with engine.connect() as conn:
        try:
            # Paso 1: Eliminar el default si existe
            logger.info("Paso 1: Eliminando default de user_id...")
            conn.execute(text("""
                ALTER TABLE transactions 
                ALTER COLUMN user_id DROP DEFAULT
            """))
            conn.commit()
            logger.info("✅ Default eliminado")
            
            # Paso 2: Cambiar el tipo de VARCHAR a UUID
            logger.info("Paso 2: Cambiando tipo de VARCHAR a UUID...")
            conn.execute(text("""
                ALTER TABLE transactions 
                ALTER COLUMN user_id TYPE UUID USING user_id::UUID
            """))
            conn.commit()
            logger.info("✅ Tipo cambiado a UUID")
            
            # Paso 3: Verificar que no haya datos inválidos
            result = conn.execute(text("""
                SELECT COUNT(*) FROM transactions 
                WHERE user_id IS NULL
            """))
            null_count = result.scalar()
            if null_count > 0:
                logger.warning(f"⚠️ Hay {null_count} registros con user_id NULL")
            else:
                logger.info("✅ Todos los user_id son válidos")
            
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            conn.rollback()
            raise
    
    logger.info("🎉 Migración completada exitosamente")

if __name__ == "__main__":
    main()

