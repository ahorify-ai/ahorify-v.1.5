# 🔄 Guía de Migración: SQLite → PostgreSQL

Esta guía explica cómo configurar y usar la nueva base de datos PostgreSQL.

## 📋 Archivos Creados

1. **`core/database_postgres.py`** - Clase Database adaptada para PostgreSQL
2. **`core/config_db.py`** - Configuración de conexión PostgreSQL
3. **`test_postgres_connection.py`** - Script de prueba de conexión
4. **`requirements.txt`** - Actualizado con `psycopg2-binary`

## 🔧 Configuración

### Paso 1: Obtener URL de conexión PostgreSQL

Si usas **Neon** o **Supabase**, obtén la connection string desde el dashboard.

**Formato de URL:**
```
postgresql://usuario:password@host:puerto/database?sslmode=require
```

**Ejemplo Neon:**
```
postgresql://usuario:pass@ep-cool-darkness-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### Paso 2: Configurar variable de entorno

**Opción A: Variable de entorno del sistema**
```bash
export DATABASE_URL='postgresql://usuario:pass@host:port/database'
```

**Opción B: Archivo .env (recomendado)**
Crea un archivo `.env` en la raíz del proyecto:
```
DATABASE_URL=postgresql://usuario:pass@host:port/database
```

Luego carga las variables antes de ejecutar:
```bash
source .env  # Linux/Mac
# O usa python-dotenv para cargar automáticamente
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

Esto instalará `psycopg2-binary` necesario para PostgreSQL.

### Paso 4: Probar la conexión

```bash
python test_postgres_connection.py
```

Si todo está bien, verás:
```
✅ ¡Conexión exitosa!
```

## 🔄 Cambios Principales SQLite → PostgreSQL

### Placeholders
- **SQLite:** `?` → **PostgreSQL:** `%s`

### Tipos de Datos
- **TEXT** → **VARCHAR** o **TEXT** (ambos funcionan)
- **REAL** → **NUMERIC(10, 2)**
- **INTEGER** → **INTEGER** (igual)
- **BOOLEAN** → **BOOLEAN** (igual)
- **TIMESTAMP** → **TIMESTAMP** (igual)

### Sintaxis Específica
- `INSERT OR IGNORE` → `ON CONFLICT DO NOTHING`
- `INSERT OR REPLACE` → `ON CONFLICT DO UPDATE`
- `date(created_at)` → `DATE(created_at)` o `created_at::date`
- `PRAGMA table_info()` → Consulta a `information_schema`

### Ejemplo de Query Adaptada

**Antes (SQLite):**
```python
cursor.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
```

**Ahora (PostgreSQL):**
```python
cursor.execute("SELECT * FROM transactions WHERE user_id = %s", (user_id,))
```

## 📦 Uso en el Código

### Para usar PostgreSQL en lugar de SQLite:

**Antes:**
```python
from core.database import db  # SQLite
```

**Ahora:**
```python
from core.database_postgres import db  # PostgreSQL
```

La interfaz es **exactamente la misma**, solo cambias el import.

## ✅ Validación

Puedes validar que todo funciona:

1. **Conexión:**
   ```bash
   python test_postgres_connection.py
   ```

2. **Crear una transacción de prueba:**
   ```python
   from core.database_postgres import db
   
   db.save_transaction({
       'id': 'test-123',
       'user_id': 'default_user',
       'amount': 25.50,
       'type': 'expense',
       'category': '🍔 Comida',
       'emotion': 'neutral'
   })
   ```

3. **Verificar en tu dashboard de Neon/Supabase:**
   - Deberías ver las tablas creadas automáticamente
   - Y la transacción de prueba

## 🚨 Troubleshooting

### Error: "DATABASE_URL not configured"
- Verifica que la variable de entorno esté configurada
- Prueba con: `echo $DATABASE_URL`

### Error: "connection refused"
- Verifica que la URL de conexión sea correcta
- Asegúrate de que el servidor PostgreSQL esté accesible
- En Neon/Supabase, verifica que la IP esté permitida

### Error: "module psycopg2 not found"
- Instala: `pip install psycopg2-binary`

## 📝 Notas

- El código actual de SQLite (`core/database.py`) **NO se modifica**
- Puedes mantener ambas versiones funcionando en paralelo
- Para cambiar completamente a PostgreSQL, solo cambia los imports
- Las tablas se crean automáticamente la primera vez que conectas

