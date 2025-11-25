# api/v1/helpers.py
"""
Helper functions para endpoints
"""

from sqlalchemy.orm import Session
from api.models import User
from typing import Optional

def get_user_by_google_id(db: Session, google_id: str) -> Optional[User]:
    """
    Helper para obtener usuario por Google ID
    Retorna el User o None si no existe
    """
    return db.query(User).filter(User.google_id == google_id).first()

