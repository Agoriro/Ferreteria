"""
Script para probar la conexion a la base de datos.
Ejecutar: python test_db_connection.py
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("=" * 50)
print("PRUEBA DE CONEXION A BASE DE DATOS")
print("=" * 50)

if not DATABASE_URL:
    print("[ERROR] No se encontro DATABASE_URL en .env")
    print("   Asegurate de tener un archivo .env con:")
    print("   DATABASE_URL=postgresql://usuario:contrasena@host:puerto/basedatos")
    exit(1)

# Ocultar contrasena para mostrar
display_url = DATABASE_URL
if "@" in DATABASE_URL:
    parts = DATABASE_URL.split("@")
    prefix = parts[0].split(":")
    if len(prefix) >= 3:
        display_url = f"{prefix[0]}:{prefix[1]}:****@{parts[1]}"

print(f"URL: {display_url}")
print()

# Probar conexion sincrona con psycopg2
print("Probando conexion con psycopg2...")
try:
    import psycopg2
    
    # Parsear URL
    url = DATABASE_URL.replace("postgresql://", "")
    user_pass, host_db = url.split("@")
    user, password = user_pass.split(":")
    host_port, database = host_db.split("/")
    
    if ":" in host_port:
        host, port = host_port.split(":")
    else:
        host = host_port
        port = "5432"
    
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    
    print(f"[OK] CONEXION EXITOSA!")
    print(f"   PostgreSQL: {version[:60]}...")
    
    # Verificar tablas existentes
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = cursor.fetchall()
    
    print()
    if tables:
        print(f"Tablas encontradas ({len(tables)}):")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"   - {table[0]} ({count} registros)")
    else:
        print("[AVISO] No hay tablas en la base de datos.")
        print("   Necesitas ejecutar las migraciones o scripts SQL.")
    
    cursor.close()
    conn.close()
    
except psycopg2.OperationalError as e:
    print(f"[ERROR] ERROR DE CONEXION:")
    print(f"   {str(e)}")
    print()
    print("Posibles causas:")
    print("   1. PostgreSQL no esta corriendo")
    print("   2. Host/Puerto incorrectos")
    print("   3. Usuario/Contrasena incorrectos")
    print("   4. Base de datos no existe")
    
except Exception as e:
    print(f"[ERROR] {type(e).__name__}")
    print(f"   {str(e)}")

print()
print("=" * 50)
