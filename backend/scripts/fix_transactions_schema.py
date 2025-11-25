#!/usr/bin/env python3
"""
Script para corregir el esquema de la tabla transactions:
- Cambiar id y user_id de VARCHAR a UUID
- Hacer emotion nullable
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.database import engine
from sqlalchemy import text, inspect
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Ejecuta la migración"""
    logger.info("🚀 Iniciando corrección del esquema de transactions...")
    
    with engine.connect() as conn:
        inspector = inspect(engine)
        
        if 'transactions' not in inspector.get_table_names():
            logger.error("❌ La tabla 'transactions' no existe")
            return
        
        # Obtener información actual
        columns = {col['name']: col for col in inspector.get_columns('transactions')}
        
        # 1. Cambiar user_id de VARCHAR a UUID
        if 'user_id' in columns:
            current_type = str(columns['user_id']['type'])
            if 'VARCHAR' in current_type or 'CHARACTER VARYING' in current_type:
                logger.info("🔄 Cambiando user_id de VARCHAR a UUID...")
                try:
                    # Primero, convertir los valores existentes a UUID si es posible
                    conn.execute(text("""
                        ALTER TABLE transactions 
                        ALTER COLUMN user_id TYPE UUID USING user_id::UUID
                    """))
                    conn.commit()
                    logger.info("✅ user_id cambiado a UUID correctamente")
                except Exception as e:
                    logger.error(f"❌ Error cambiando user_id: {e}")
                    conn.rollback()
            else:
                logger.info("✅ user_id ya es UUID")
        
        # 2. Cambiar id de VARCHAR a UUID
        if 'id' in columns:
            current_type = str(columns['id']['type'])
            if 'VARCHAR' in current_type or 'CHARACTER VARYING' in current_type:
                logger.info("🔄 Cambiando id de VARCHAR a UUID...")
                try:
                    conn.execute(text("""
                        ALTER TABLE transactions 
                        ALTER COLUMN id TYPE UUID USING id::UUID
                    """))
                    conn.commit()
                    logger.info("✅ id cambiado a UUID correctamente")
                except Exception as e:
                    logger.error(f"❌ Error cambiando id: {e}")
                    conn.rollback()
            else:
                logger.info("✅ id ya es UUID")
        
        # 3. Hacer emotion nullable
        if 'emotion' in columns:
            if not columns['emotion'].get('nullable', True):
                logger.info("🔄 Haciendo emotion nullable...")
                try:
                    # Primero, establecer valores NULL a un valor por defecto si es necesario
                    conn.execute(text("""
                        UPDATE transactions 
                        SET emotion = NULL 
                        WHERE emotion IS NULL OR emotion = ''
                    """))
                    conn.commit()
                    
                    # Luego, hacer la columna nullable
                    conn.execute(text("""
                        ALTER TABLE transactions 
                        ALTER COLUMN emotion DROP NOT NULL
                    """))
                    conn.commit()
                    logger.info("✅ emotion ahora es nullable")
                except Exception as e:
                    logger.error(f"❌ Error haciendo emotion nullable: {e}")
                    conn.rollback()
            else:
                logger.info("✅ emotion ya es nullable")
        
        # 4. Verificar que raw_text no sea NULL si está vacío
        if 'raw_text' in columns:
            if columns['raw_text'].get('nullable', True):
                logger.info("🔄 Verificando raw_text...")
                try:
                    # Establecer valores vacíos a un texto por defecto
                    conn.execute(text("""
                        UPDATE transactions 
                        SET raw_text = 'Sin descripción' 
                        WHERE raw_text IS NULL OR raw_text = ''
                    """))
                    conn.commit()
                    
                    # Hacer NOT NULL si el modelo lo requiere
                    conn.execute(text("""
                        ALTER TABLE transactions 
                        ALTER COLUMN raw_text SET NOT NULL
                    """))
                    conn.commit()
                    logger.info("✅ raw_text ahora es NOT NULL")
                except Exception as e:
                    logger.error(f"⚠️ Error con raw_text: {e}")
                    conn.rollback()
    
    logger.info("🎉 Corrección del esquema completada")

if __name__ == "__main__":
    main()

