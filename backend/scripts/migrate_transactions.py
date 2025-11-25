#!/usr/bin/env python3
"""
Script de migración para agregar columnas faltantes a la tabla transactions
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.database import engine
from sqlalchemy import text, inspect
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def column_exists(conn, table_name, column_name):
    """Verifica si una columna existe en una tabla"""
    inspector = inspect(engine)
    try:
        columns = [col['name'] for col in inspector.get_columns(table_name)]
        return column_name in columns
    except:
        return False

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
    logger.info("🚀 Iniciando migración de tabla transactions...")
    
    with engine.connect() as conn:
        inspector = inspect(engine)
        
        # Verificar que la tabla transactions existe
        if 'transactions' not in inspector.get_table_names():
            logger.error("❌ La tabla 'transactions' no existe. Creándola...")
            from api.database import Base
            from api.models import Transaction
            Base.metadata.create_all(bind=engine, tables=[Transaction.__table__])
            logger.info("✅ Tabla transactions creada")
        
        changes_made = False
        
        # Columnas necesarias para transactions según el modelo
        columns_to_add = [
            ('raw_text', 'TEXT'),
            ('amount', 'NUMERIC(10, 2)'),
            ('category', 'VARCHAR(255)'),
            ('type', 'VARCHAR(20)'),
            ('aury_response', 'TEXT'),
        ]
        
        for col_name, col_def in columns_to_add:
            if add_column_if_not_exists(conn, 'transactions', col_name, col_def):
                changes_made = True
        
        if not changes_made:
            logger.info("✅ Todas las columnas ya existen. No se requieren cambios.")
        else:
            logger.info("✅ Migración completada exitosamente")
    
    logger.info("🎉 Proceso finalizado")

if __name__ == "__main__":
    main()

