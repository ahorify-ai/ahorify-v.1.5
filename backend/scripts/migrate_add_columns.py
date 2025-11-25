#!/usr/bin/env python3
"""
Script de migración para agregar columnas faltantes a la base de datos
Agrega columnas de forma segura sin perder datos existentes
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.database import engine
from sqlalchemy import text, inspect
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def column_exists(conn, table_name, column_name):
    """Verifica si una columna existe en una tabla"""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def add_column_if_not_exists(conn, table_name, column_name, column_definition):
    """Agrega una columna si no existe"""
    if column_exists(conn, table_name, column_name):
        logger.info(f"✅ Columna {table_name}.{column_name} ya existe")
        return False
    
    try:
        conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}"))
        conn.commit()
        logger.info(f"✅ Columna {table_name}.{column_name} agregada correctamente")
        return True
    except Exception as e:
        logger.error(f"❌ Error agregando {table_name}.{column_name}: {e}")
        conn.rollback()
        return False

def main():
    """Ejecuta la migración"""
    logger.info("🚀 Iniciando migración de base de datos...")
    
    with engine.connect() as conn:
        # Verificar que la tabla users existe
        inspector = inspect(engine)
        if 'users' not in inspector.get_table_names():
            logger.error("❌ La tabla 'users' no existe. Ejecuta primero: Base.metadata.create_all()")
            return
        
        changes_made = False
        
        # Agregar google_id si no existe
        if add_column_if_not_exists(conn, 'users', 'google_id', 'VARCHAR(255)'):
            changes_made = True
        
        # Agregar aury_tone si no existe
        if add_column_if_not_exists(conn, 'users', 'aury_tone', "VARCHAR(20) DEFAULT 'sarcastic' NOT NULL"):
            changes_made = True
        
        # Verificar otras columnas importantes
        required_columns = {
            'email': 'VARCHAR(255)',
            'goal': 'TEXT',
            'is_plus_user': 'BOOLEAN DEFAULT FALSE NOT NULL',
            'last_weekly_freeze_date': 'DATE',
            'weekly_freeze_count': 'INTEGER DEFAULT 0 NOT NULL',
            'streak_freezes_available': 'INTEGER DEFAULT 0 NOT NULL',
        }
        
        for col_name, col_def in required_columns.items():
            if not column_exists(conn, 'users', col_name):
                logger.warning(f"⚠️ Columna users.{col_name} no existe. Considera agregarla manualmente.")
        
        if not changes_made:
            logger.info("✅ Todas las columnas ya existen. No se requieren cambios.")
        else:
            logger.info("✅ Migración completada exitosamente")
    
    logger.info("🎉 Proceso finalizado")

if __name__ == "__main__":
    main()

