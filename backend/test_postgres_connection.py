# test_postgres_connection.py
"""
Script de prueba rápida para validar la conexión a PostgreSQL
Ejecutar: python test_postgres_connection.py
"""

import os
import sys

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(__file__))

# Cargar variables de entorno desde .env ANTES de importar database
try:
    from dotenv import load_dotenv
    load_dotenv()  # Carga el archivo .env
except ImportError:
    pass  # Si python-dotenv no está, intentará usar variables de entorno del sistema

def test_connection():
    """Prueba la conexión a PostgreSQL"""
    print("🧪 Probando conexión a PostgreSQL...")
    print("-" * 50)
    
    # Verificar variable de entorno
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ ERROR: Variable de entorno DATABASE_URL no configurada")
        print("\n💡 Cómo configurarla:")
        print("   export DATABASE_URL='postgresql://user:pass@host:port/database'")
        print("\n   O crea un archivo .env con:")
        print("   DATABASE_URL=postgresql://user:pass@host:port/database")
        return False
    
    print(f"✅ DATABASE_URL encontrada: {database_url[:30]}...")
    
    try:
        from core.database_postgres import db
        
        print("\n📡 Intentando conectar a PostgreSQL...")
        if db.test_connection():
            print("✅ ¡Conexión exitosa!")
            
            # Probar una query simple
            print("\n📊 Probando query simple...")
            stats = db.get_user_stats("default_user")
            if stats:
                print(f"✅ Query exitosa. Stats encontrados: {stats}")
            else:
                print("ℹ️  No hay stats aún (tabla vacía o usuario no existe)")
            
            return True
        else:
            print("❌ Error en la conexión")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\n💡 Verifica:")
        print("   1. Que DATABASE_URL sea correcta")
        print("   2. Que el servidor PostgreSQL esté accesible")
        print("   3. Que las credenciales sean correctas")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)

