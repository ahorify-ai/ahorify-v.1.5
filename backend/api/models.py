# api/models.py
"""
Modelos SQLAlchemy para Ahorify V1.5
Diseñados para las 10 features core del pivot
"""

from sqlalchemy import Column, String, Integer, Numeric, Boolean, Text, Date, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, date
import uuid
from api.database import Base

class User(Base):
    """
    Modelo de Usuario - Feature 1, 3, 9
    - Google Auth (Feature 1): google_id como identificador principal
    - User Goal (Feature 3)
    - Freemium Model (Feature 9) - V2.0 (comentado)
    """
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # PK interno (no se usa en API)
    google_id = Column(String(255), unique=True, nullable=True)  # Feature 1: Google ID (sub) - identificador principal
    email = Column(String(255), unique=True, nullable=True)  # Email de Google
    goal = Column(Text, nullable=True)  # Feature 3: "¿Para qué ahorras?"
    
    # TODO V2.0: Descomentar cuando se implemente Feature 9 (Freemium)
    # is_plus_user = Column(Boolean, default=False, nullable=False)  # Feature 9: Freemium
    # V1.5: Campo mantenido en DB pero siempre False (no usado en lógica)
    is_plus_user = Column(Boolean, default=False, nullable=False, server_default='false')
    
    # V1.5: Protector semanal gratuito (1 uso por semana)
    last_weekly_freeze_date = Column(Date, nullable=True)  # Fecha de último uso del freeze semanal
    weekly_freeze_count = Column(Integer, default=0, nullable=False)  # Veces usadas en la semana actual
    
    # Aury Tone Preference: 'sarcastic', 'subtle', 'analytical'
    aury_tone = Column(String(20), default='sarcastic', nullable=False, server_default='sarcastic')
    
    # Deprecated V1.5: Mantener por compatibilidad pero no usar
    streak_freezes_available = Column(Integer, default=0, nullable=False, server_default='0')
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    streak = relationship("Streak", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class Transaction(Base):
    """
    Modelo de Transacción - Feature 4, 5, 7
    - Smart Text Input (Feature 4): raw_text
    - Aury Parser (Feature 5): amount, category parseados
    - Feed con Roast (Feature 7): aury_response
    """
    __tablename__ = "transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Feature 4: Smart Input - texto libre del usuario
    raw_text = Column(Text, nullable=False)
    
    # Feature 5: Parseado por Aury/DeepSeek
    amount = Column(Numeric(10, 2), nullable=True)  # Nullable hasta que se parse
    category = Column(String(255), nullable=True)
    type = Column(String(20), nullable=True)  # 'expense' o 'income'
    
    # Feature 7: Comentario sarcástico de Aury
    aury_response = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("amount IS NULL OR amount > 0", name="check_positive_amount"),
        CheckConstraint("type IS NULL OR type IN ('expense', 'income')", name="check_valid_type"),
    )
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, user_id={self.user_id}, amount={self.amount})>"


class Streak(Base):
    """
    Modelo de Racha - Feature 6, 8
    - Dashboard Racha Centrado (Feature 6)
    - Lógica Racha Resiliente (Feature 8)
    """
    __tablename__ = "streaks"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    current_streak = Column(Integer, default=0, nullable=False)
    longest_streak = Column(Integer, default=0, nullable=False)
    last_activity_date = Column(Date, nullable=True)  # NULL si nunca ha tenido actividad
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Constraints
    __table_args__ = (
        CheckConstraint("current_streak >= 0", name="check_positive_current_streak"),
        CheckConstraint("longest_streak >= 0", name="check_positive_longest_streak"),
    )
    
    # Relationships
    user = relationship("User", back_populates="streak")
    
    def __repr__(self):
        return f"<Streak(user_id={self.user_id}, current={self.current_streak}, longest={self.longest_streak})>"


class DeviceSubscription(Base):
    """
    Modelo para suscripciones de dispositivos - Feature 10
    Almacena tokens de OneSignal para enviar notificaciones push
    """
    __tablename__ = "device_subscriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    onesignal_player_id = Column(String(255), unique=True, nullable=False)  # OneSignal Player ID
    device_type = Column(String(50), nullable=True)  # 'web', 'ios', 'android'
    user_agent = Column(Text, nullable=True)  # Para debugging
    is_active = Column(Boolean, default=True, nullable=False)  # Para desactivar sin borrar
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="device_subscriptions")
    
    def __repr__(self):
        return f"<DeviceSubscription(user_id={self.user_id}, player_id={self.onesignal_player_id})>"

