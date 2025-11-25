# run_api.py
"""
Script para ejecutar FastAPI fácilmente
"""

import uvicorn

if __name__ == "__main__":
    print("🚀 Iniciando Ahorify API V1.5...")
    print("📚 Documentación: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/")
    print("\nPresiona Ctrl+C para detener\n")
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

