# api/schemas.py
"""
Schemas Pydantic para Request/Response
Validación y serialización para las 10 features core
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID

# ==================== FEATURE 4: SMART INPUT ====================
class GastoCreateRequest(BaseModel):
    """Feature 4: Request para Smart Text Input"""
    raw_text: str = Field(..., min_length=1, max_length=500, description="Texto libre del usuario: 'Pizza 15 euros'")
    google_id: str = Field(..., description="Google ID del usuario autenticado")

class GastoResponse(BaseModel):
    """Response después de crear gasto - Feature 4, 5, 7"""
    success: bool
    transaction_id: UUID
    parsed_data: Optional[dict] = Field(None, description="Datos parseados: amount, category, type")
    aury_response: Optional[str] = Field(None, description="Feature 7: Comentario sarcástico de Aury")
    message: str

# ==================== FEATURE 6, 8: RACHA ====================
class RachaResponse(BaseModel):
    """Feature 6: Dashboard Racha Centrado"""
    google_id: str = Field(..., description="Google ID del usuario")
    current_streak: int = Field(..., ge=0)
    longest_streak: int = Field(..., ge=0)
    freeze_inventory: int = Field(..., ge=0, description="V1.5: 1 si tiene protector semanal disponible, 0 si no")
    is_plus_user: bool = Field(default=False, description="V1.5: Siempre False. TODO V2.0: Feature 9 (Freemium)")
    last_activity_date: Optional[date]

# ==================== FEATURE 7: FEED CON ROAST ====================
class GastoFeedItem(BaseModel):
    """Feature 7: Item del feed con roast de Aury"""
    id: UUID
    amount: Optional[float]
    category: Optional[str]
    raw_text: str
    aury_response: Optional[str]
    created_at: datetime

class GastoFeedResponse(BaseModel):
    """Response del feed de gastos"""
    gastos: List[GastoFeedItem]
    total: int

# ==================== FEATURE 1: GOOGLE AUTH ====================
class GoogleAuthRequest(BaseModel):
    """Feature 1: Request de autenticación Google"""
    token: str = Field(..., description="Google ID Token")

class GoogleAuthResponse(BaseModel):
    """Response de autenticación Google - Opción B: Usa Google ID"""
    google_id: str = Field(..., description="Google ID (sub) - identificador principal")
    email: str
    is_new_user: bool
    message: str

# ==================== FEATURE 2: WAITLIST ====================
class WaitlistStatusResponse(BaseModel):
    """Feature 2: Estado de la lista de espera"""
    on_waitlist: bool
    total_users: int
    waitlist_limit: int

class BetaStatusResponse(BaseModel):
    """Estado de slots disponibles para Beta"""
    slots_remaining: int

# ==================== FEATURE 3: USER GOAL ====================
class UserGoalRequest(BaseModel):
    """Feature 3: Guardar objetivo del usuario"""
    goal: str = Field(..., min_length=1, max_length=500, description="¿Para qué ahorras?")

class UserGoalResponse(BaseModel):
    """Response de guardar goal"""
    success: bool
    goal: str
    message: str

# ==================== AURY TONE PREFERENCE ====================
class AuryToneRequest(BaseModel):
    """Request para cambiar el tono de Aury"""
    google_id: str = Field(..., description="Google ID del usuario")
    tone: str = Field(..., description="Tono de Aury: 'sarcastic', 'subtle', 'analytical'")
    
    @validator('tone')
    def validate_tone(cls, v):
        valid_tones = ['sarcastic', 'subtle', 'analytical']
        if v not in valid_tones:
            raise ValueError(f"Tono debe ser uno de: {', '.join(valid_tones)}")
        return v

class AuryToneResponse(BaseModel):
    """Response de cambiar tono de Aury"""
    success: bool
    tone: str
    message: str

# ==================== FEATURE 8: STREAK FREEZE ====================
class StreakFreezeRequest(BaseModel):
    """Feature 8: Usar protector semanal para proteger racha"""
    google_id: str = Field(..., description="Google ID del usuario")

class StreakFreezeResponse(BaseModel):
    """Response de usar freeze"""
    success: bool
    freeze_used: bool
    remaining_freezes: int
    message: str

# ==================== FEATURE 9: FREEMIUM (V2.0 - COMENTADO) ====================
# TODO V2.0: Descomentar cuando se implemente modelo Freemium
# class SubscriptionResponse(BaseModel):
#     """Feature 9: Estado de suscripción del usuario"""
#     user_id: UUID
#     is_plus_user: bool
#     streak_freezes_available: int
#     has_unlimited_freezes: bool

# ==================== FEATURE 10: PUSH NOTIFICATIONS ====================
class DeviceSubscriptionRequest(BaseModel):
    """Feature 10: Request para suscribir dispositivo a notificaciones"""
    google_id: str = Field(..., description="Google ID del usuario")
    player_id: str = Field(..., description="OneSignal Player ID")
    device_type: Optional[str] = Field(default="web", description="Tipo de dispositivo: web, ios, android")
    user_agent: Optional[str] = Field(None, description="User agent del navegador")

class DeviceSubscriptionResponse(BaseModel):
    """Response de suscripción de dispositivo"""
    success: bool
    subscription_id: str
    message: str

# ==================== HEALTH CHECK ====================
class HealthCheckResponse(BaseModel):
    """Health check del API"""
    status: str
    database: str
    version: str
    timestamp: datetime

