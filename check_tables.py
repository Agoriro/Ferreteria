"""Verificar tablas en schema public"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
url = DATABASE_URL.replace("postgresql://", "")
user_pass, host_db = url.split("@")
user, password = user_pass.split(":")
host_port, database = host_db.split("/")
host, port = host_port.split(":") if ":" in host_port else (host_port, "5432")

conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
cur = conn.cursor()

print("=" * 50)
print("TABLAS EN SCHEMA 'public':")
print("=" * 50)

cur.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    ORDER BY table_name
""")
tables = cur.fetchall()

for t in tables:
    cur.execute(f'SELECT COUNT(*) FROM "public"."{t[0]}"')
    count = cur.fetchone()[0]
    print(f"  - {t[0]} ({count} registros)")

# Verificar si hay usuarios
print()
print("=" * 50)
print("USUARIOS EN LA TABLA:")
print("=" * 50)

try:
    cur.execute('SELECT id, username, estado FROM "public".usuarios')
    users = cur.fetchall()
    if users:
        for u in users:
            print(f"  ID: {u[0]}, Username: {u[1]}, Activo: {u[2]}")
    else:
        print("  [AVISO] No hay usuarios creados!")
except Exception as e:
    print(f"  [ERROR] {e}")

cur.close()
conn.close()

