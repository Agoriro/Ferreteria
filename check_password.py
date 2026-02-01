"""Verificar password del usuario admin"""
import os
import psycopg2
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

# Configurar passlib igual que en el proyecto
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DATABASE_URL = os.getenv("DATABASE_URL")
url = DATABASE_URL.replace("postgresql://", "")
user_pass, host_db = url.split("@")
user, password = user_pass.split(":")
host_port, database = host_db.split("/")
host, port = host_port.split(":") if ":" in host_port else (host_port, "5432")

conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
cur = conn.cursor()

cur.execute('SELECT username, password FROM "public".usuarios WHERE username = %s', ('admin',))
result = cur.fetchone()

if result:
    username, hashed_password = result
    print(f"Usuario: {username}")
    print(f"Hash almacenado: {hashed_password[:50]}...")
    print()
    
    # Probar con diferentes passwords
    test_passwords = ["admin123", "admin", "Admin123", "password", "123456"]
    
    print("Probando passwords:")
    for test_pwd in test_passwords:
        is_valid = pwd_context.verify(test_pwd, hashed_password)
        status = "[OK] CORRECTA!" if is_valid else "[X]"
        print(f"  {status} '{test_pwd}'")
        if is_valid:
            break
else:
    print("[ERROR] Usuario 'admin' no encontrado")

cur.close()
conn.close()

