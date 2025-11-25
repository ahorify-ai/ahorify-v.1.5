# test_fastapi.py
"""
Script de prueba rápida para FastAPI
Verifica que la API esté funcionando
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Prueba el health check endpoint"""
    print("🧪 Probando Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check OK")
            print(f"   Status: {data['status']}")
            print(f"   Database: {data['database']}")
            print(f"   Version: {data['version']}")
            return True
        else:
            print(f"❌ Health Check falló: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al servidor")
        print("   ¿Está corriendo FastAPI? Ejecuta: uvicorn api.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_waitlist():
    """Prueba el endpoint de waitlist"""
    print("\n🧪 Probando Waitlist Status...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/waitlist/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Waitlist Status OK")
            print(f"   Total usuarios: {data['total_users']}")
            print(f"   En waitlist: {data['on_waitlist']}")
            print(f"   Límite: {data['waitlist_limit']}")
            return True
        else:
            print(f"❌ Waitlist falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_docs():
    """Verifica que la documentación esté disponible"""
    print("\n🧪 Verificando documentación...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ Documentación disponible en: http://localhost:8000/docs")
            return True
        else:
            print(f"⚠️  Docs no disponible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Test de FastAPI - Ahorify V1.5")
    print("=" * 50)
    
    results = []
    results.append(test_health_check())
    results.append(test_waitlist())
    results.append(test_docs())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ Todos los tests pasaron")
    else:
        print("⚠️  Algunos tests fallaron")
    print("=" * 50)

