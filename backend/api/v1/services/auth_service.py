# api/v1/services/auth_service.py
"""
Auth Service - Feature 1
Validación de Google OAuth Token y gestión de usuarios
"""

from typing import Dict, Optional, Tuple
from sqlalchemy.orm import Session
from api.models import User
from api.config import GOOGLE_CLIENT_ID
import logging

logger = logging.getLogger(__name__)

# Importar librerías de Google Auth (opcional si no están instaladas)
try:
    from google.auth.transport import requests as google_requests
    from google.oauth2 import id_token
    GOOGLE_AUTH_AVAILABLE = True
except ImportError:
    GOOGLE_AUTH_AVAILABLE = False
    logger.warning("google-auth no instalado. Instala con: pip install google-auth")

class AuthService:
    """
    Feature 1: Servicio de autenticación Google
    """
    
    @staticmethod
    def verify_google_token(token: str) -> Optional[Dict]:
        """
        Verifica y decodifica el token de Google OAuth
        Retorna payload del token si es válido, None si no
        """
        try:
            # Si GOOGLE_CLIENT_ID no está configurado, usar modo desarrollo
            if not GOOGLE_CLIENT_ID or not GOOGLE_AUTH_AVAILABLE:
                logger.warning("GOOGLE_CLIENT_ID no configurado o google-auth no instalado")
                logger.warning("Modo desarrollo: decodificando token sin verificación")
                # Para desarrollo/testing, intentar decodificar sin verificar
                try:
                    import jwt
                    # Decodificar sin verificar (solo para desarrollo)
                    payload = jwt.decode(token, options={"verify_signature": False})
                    # Validar estructura básica
                    if 'sub' in payload and 'email' in payload:
                        return payload
                    else:
                        logger.error("Token no contiene 'sub' o 'email'")
                        return None
                except ImportError:
                    logger.error("PyJWT no instalado. Instala con: pip install PyJWT")
                    return None
                except Exception as e:
                    logger.error(f"Error decodificando token: {e}")
                    return None
            
            # Verificación real con Google (producción)
            idinfo = id_token.verify_oauth2_token(
                token, 
                google_requests.Request(), 
                GOOGLE_CLIENT_ID
            )
            
            # Verificar que el token es de Google
            if idinfo.get('iss') not in ['accounts.google.com', 'https://accounts.google.com']:
                logger.error(f"Token issuer inválido: {idinfo.get('iss')}")
                return None
            
            return idinfo
            
        except ValueError as e:
            logger.error(f"Token de Google inválido: {e}")
            return None
        except Exception as e:
            logger.error(f"Error verificando token de Google: {e}")
            return None
    
    @staticmethod
    def get_or_create_user(db: Session, google_id: str, email: str) -> Tuple[User, bool]:
        """
        Obtiene o crea un usuario basado en Google ID
        Retorna: (User, is_new_user)
        """
        # Buscar usuario por google_id
        user = db.query(User).filter(User.google_id == google_id).first()
        
        if user:
            # Usuario existe, actualizar email por si cambió
            if user.email != email:
                user.email = email
                db.commit()
                db.refresh(user)
            return user, False
        
        # Crear nuevo usuario
        user = User(
            google_id=google_id,
            email=email,
            is_plus_user=False,
            weekly_freeze_count=0,
            streak_freezes_available=0
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"✅ Nuevo usuario creado: {email} (google_id: {google_id})")
        return user, True
    
    @staticmethod
    def authenticate_google_token(db: Session, token: str) -> Optional[Tuple[User, bool]]:
        """
        Autentica un token de Google y retorna el usuario (o lo crea si no existe)
        Retorna: (User, is_new_user) o None si el token es inválido
        """
        # Verificar token
        idinfo = AuthService.verify_google_token(token)
        
        if not idinfo:
            return None
        
        # Extraer información del token
        google_id = idinfo.get('sub')  # Google ID único
        email = idinfo.get('email')
        
        if not google_id:
            logger.error("Token de Google no contiene 'sub' (Google ID)")
            return None
        
        if not email:
            logger.error("Token de Google no contiene 'email'")
            return None
        
        # Obtener o crear usuario
        user, is_new_user = AuthService.get_or_create_user(db, google_id, email)
        
        return user, is_new_user
    
    @staticmethod
    def get_user_by_google_id(db: Session, google_id: str) -> Optional[User]:
        """
        Obtiene un usuario por su Google ID
        """
        return db.query(User).filter(User.google_id == google_id).first()

