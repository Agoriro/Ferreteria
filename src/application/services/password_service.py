"""
Servicio de gestión de contraseñas.
Principio SOLID: Single Responsibility - Solo maneja hashing de passwords.
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordService:
    """Servicio para hash y verificación de contraseñas."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Genera hash de contraseña."""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica contraseña contra hash."""
        return pwd_context.verify(plain_password, hashed_password)
