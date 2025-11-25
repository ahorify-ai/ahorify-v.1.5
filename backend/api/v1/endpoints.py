# api/v1/endpoints.py
"""
Endpoints V1 - Todas las rutas agrupadas para las 10 features core
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import date, timedelta

from api.database import get_db
from api.models import User, Transaction, Streak, DeviceSubscription
from api.schemas import (
    GastoCreateRequest, GastoResponse, GastoFeedResponse, GastoFeedItem,
    RachaResponse, WaitlistStatusResponse, UserGoalRequest, UserGoalResponse,
    StreakFreezeRequest, StreakFreezeResponse,
    DeviceSubscriptionRequest, DeviceSubscriptionResponse,
    BetaStatusResponse,
    AuryToneRequest, AuryToneResponse,
    # SubscriptionResponse,  # TODO V2.0: Descomentar cuando se implemente Feature 9
    GoogleAuthRequest, GoogleAuthResponse
)
from api.config import WAITLIST_LIMIT, MAX_BETA_USERS
from api.v1.services.aury_service import parse_raw_text, generate_aury_response, parse_with_deepseek, generate_aury_with_deepseek
from api.v1.services.streak_service import StreakService
from api.v1.services.auth_service import AuthService
from api.v1.services.notification_service import NotificationService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["v1"])

# ==================== FEATURE 1: GOOGLE AUTH ====================
@router.post("/auth/google", response_model=GoogleAuthResponse, status_code=status.HTTP_201_CREATED)
async def google_auth(
    request: GoogleAuthRequest,
    db: Session = Depends(get_db)
):
    """
    Feature 1: Autenticación Google OAuth
    Valida el token de Google y crea/obtiene el usuario
    Retorna google_id como identificador principal
    """
    try:
        # Autenticar token y obtener/crear usuario
        result = AuthService.authenticate_google_token(db, request.token)
        
        if not result:
            raise HTTPException(
                status_code=401,
                detail="Token de Google inválido o expirado"
            )
        
        user, is_new_user = result
        
        return GoogleAuthResponse(
            google_id=user.google_id,
            email=user.email,
            is_new_user=is_new_user,
            message="Usuario autenticado correctamente" if not is_new_user else "¡Bienvenido a Ahorify! Usuario creado."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en autenticación Google: {e}")
        raise HTTPException(status_code=500, detail=f"Error en autenticación: {str(e)}")

# ==================== FEATURE 4, 5, 7: SMART INPUT + AURY ====================
@router.post("/gasto", response_model=GastoResponse, status_code=status.HTTP_201_CREATED)
async def crear_gasto(
    request: GastoCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Feature 4, 5, 7: Smart Text Input + Aury Parser + Feed con Roast
    Recibe texto libre, parsea con Aury, guarda transacción y genera comentario sarcástico
    """
    try:
        # Obtener usuario por Google ID
        user = AuthService.get_user_by_google_id(db, request.google_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Feature 5: Parsear texto libre (básico por ahora, DeepSeek después)
        parsed_data = await parse_with_deepseek(request.raw_text)
        
        # Obtener contexto del usuario para Aury (racha, objetivo y tono)
        streak = StreakService.get_or_create_streak(db, user.id)
        current_streak = streak.current_streak if streak else 0
        user_goal = user.goal if user.goal else None
        aury_tone = user.aury_tone if user.aury_tone else 'sarcastic'
        
        # Feature 7: Generar comentario de Aury con contexto y tono seleccionado
        aury_response = await generate_aury_with_deepseek(
            raw_text=request.raw_text,
            parsed_data=parsed_data,
            current_streak=current_streak,
            user_goal=user_goal,
            tone=aury_tone
        )
        
        # Crear transacción (usa user.id interno UUID)
        transaction = Transaction(
            user_id=user.id,  # UUID interno
            raw_text=request.raw_text,
            amount=parsed_data.get('amount'),
            category=parsed_data.get('category'),
            type=parsed_data.get('type', 'expense'),
            aury_response=aury_response
        )
        
        db.add(transaction)
        
        # Feature 8: Actualizar racha (usa user.id interno UUID)
        streak_result = StreakService.update_streak(db, user.id)
        
        db.commit()
        db.refresh(transaction)
        
        return GastoResponse(
            success=True,
            transaction_id=transaction.id,
            parsed_data=parsed_data,
            aury_response=aury_response,
            message=f"Gasto registrado. {streak_result.get('message', '')}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error registrando gasto: {e}")
        raise HTTPException(status_code=500, detail=f"Error registrando gasto: {str(e)}")

# ==================== FEATURE 7: FEED CON ROAST ====================
@router.get("/gastos/recent", response_model=GastoFeedResponse)
def get_recent_gastos(
    google_id: str,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Feature 7: Feed de gastos recientes con roast de Aury
    """
    try:
        # Obtener usuario por Google ID
        user = AuthService.get_user_by_google_id(db, google_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        transactions = db.query(Transaction)\
            .filter(Transaction.user_id == user.id)\
            .order_by(Transaction.created_at.desc())\
            .limit(limit)\
            .all()
        
        gastos = [
            GastoFeedItem(
                id=t.id,
                amount=float(t.amount) if t.amount else None,
                category=t.category,
                raw_text=t.raw_text,
                aury_response=t.aury_response,
                created_at=t.created_at
            )
            for t in transactions
        ]
        
        return GastoFeedResponse(
            gastos=gastos,
            total=len(gastos)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo gastos: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo gastos: {str(e)}")

# ==================== FEATURE 6, 8: RACHA ====================
@router.get("/racha", response_model=RachaResponse)
def get_racha(
    google_id: str,
    db: Session = Depends(get_db)
):
    """
    Feature 6: Dashboard Racha Centrado
    Feature 8: Incluye información de Freeze (Vidas Extra)
    V1.5: Sin lógica PLUS
    """
    try:
        # Obtener usuario por Google ID
        user = AuthService.get_user_by_google_id(db, google_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        streak = StreakService.get_or_create_streak(db, user.id)  # user.id es UUID interno
        
        # V1.5: Verificar si tiene protector semanal disponible
        current_date = date.today()
        has_weekly_freeze = StreakService.can_use_weekly_freeze(db, user, current_date)
        freeze_inventory = 1 if has_weekly_freeze else 0
        
        return RachaResponse(
            google_id=user.google_id,
            current_streak=streak.current_streak,
            longest_streak=streak.longest_streak,
            freeze_inventory=freeze_inventory,  # V1.5: 1 si tiene protector semanal disponible, 0 si no
            is_plus_user=False,  # V1.5: Siempre False (sin PLUS)
            last_activity_date=streak.last_activity_date
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo racha: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo racha: {str(e)}")

# ==================== FEATURE 8: STREAK FREEZE ====================
@router.post("/streak/freeze", response_model=StreakFreezeResponse)
def use_freeze(
    request: StreakFreezeRequest,
    db: Session = Depends(get_db)
):
    """
    Feature 8: Usar protector semanal para proteger racha
    V1.5: 1 protector gratis por semana (se resetea los lunes)
    TODO V2.0: Respeta modelo Freemium (Plus tiene protección ilimitada)
    """
    try:
        # Obtener usuario por Google ID
        user = AuthService.get_user_by_google_id(db, request.google_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        result = StreakService.use_freeze(db, user.id)  # user.id es UUID interno
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )
        
        return StreakFreezeResponse(
            success=result["success"],
            freeze_used=result.get("freeze_used", False),
            remaining_freezes=result.get("remaining_freezes", 0),
            message=result["message"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error usando freeze: {e}")
        raise HTTPException(status_code=500, detail=f"Error usando freeze: {str(e)}")

# ==================== FEATURE 2: WAITLIST ====================
@router.get("/waitlist/status", response_model=WaitlistStatusResponse)
def get_waitlist_status(db: Session = Depends(get_db)):
    """
    Feature 2: Escasez - Verificar si está en lista de espera
    Cuenta usuarios totales y compara con límite
    """
    try:
        total_users = db.query(User).count()
        on_waitlist = total_users >= WAITLIST_LIMIT
        
        return WaitlistStatusResponse(
            on_waitlist=on_waitlist,
            total_users=total_users,
            waitlist_limit=WAITLIST_LIMIT
        )
        
    except Exception as e:
        logger.error(f"Error verificando waitlist: {e}")
        raise HTTPException(status_code=500, detail=f"Error verificando waitlist: {str(e)}")

# ==================== PUBLIC ENDPOINTS ====================
@router.get("/public/beta-status", response_model=BetaStatusResponse)
def get_beta_status(db: Session = Depends(get_db)):
    """
    Endpoint público: Obtener slots restantes para Beta
    No requiere autenticación
    Nota: No hay límite real de usuarios, todos pueden entrar.
    Este endpoint devuelve un número alto para que el frontend muestre urgencia (68 plazas).
    """
    try:
        # Contar usuarios actuales en la base de datos
        current_users_count = db.query(User).count()
        
        # Calcular slots restantes (usando un límite muy alto para que siempre haya "plazas disponibles")
        # El frontend mostrará 68 para generar urgencia cuando hay muchos slots
        slots_remaining = max(100, MAX_BETA_USERS - current_users_count)  # Mínimo 100 para siempre mostrar urgencia
        
        return BetaStatusResponse(
            slots_remaining=slots_remaining
        )
        
    except Exception as e:
        logger.error(f"Error obteniendo estado de Beta: {e}")
        # En caso de error, devolver un valor alto para mantener urgencia
        return BetaStatusResponse(slots_remaining=100)

# ==================== FEATURE 3: USER GOAL ====================
@router.post("/user/goal", response_model=UserGoalResponse)
def set_user_goal(
    google_id: str,
    request: UserGoalRequest,
    db: Session = Depends(get_db)
):
    """
    Feature 3: Guardar objetivo del usuario (compromiso)
    """
    try:
        # Obtener usuario por Google ID
        user = AuthService.get_user_by_google_id(db, google_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        user.goal = request.goal
        db.commit()
        db.refresh(user)
        
        return UserGoalResponse(
            success=True,
            goal=user.goal,
            message="Objetivo guardado correctamente"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error guardando goal: {e}")
        raise HTTPException(status_code=500, detail=f"Error guardando goal: {str(e)}")

# ==================== AURY TONE PREFERENCE ====================
@router.post("/user/aury-tone", response_model=AuryToneResponse)
def set_aury_tone(
    request: AuryToneRequest,
    db: Session = Depends(get_db)
):
    """
    Cambiar el tono de Aury del usuario
    Tonos disponibles: 'sarcastic', 'subtle', 'analytical'
    """
    try:
        # Obtener usuario por Google ID
        user = AuthService.get_user_by_google_id(db, request.google_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Validar y actualizar tono
        user.aury_tone = request.tone
        db.commit()
        db.refresh(user)
        
        tone_names = {
            'sarcastic': 'Sarcástico',
            'subtle': 'Sutil (Madre Decepcionada)',
            'analytical': 'Analítico'
        }
        
        return AuryToneResponse(
            success=True,
            tone=user.aury_tone,
            message=f"Tono de Aury cambiado a: {tone_names.get(user.aury_tone, user.aury_tone)}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error cambiando tono de Aury: {e}")
        raise HTTPException(status_code=500, detail=f"Error cambiando tono: {str(e)}")

@router.get("/user/aury-tone")
def get_aury_tone(
    google_id: str,
    db: Session = Depends(get_db)
):
    """
    Obtener el tono actual de Aury del usuario
    """
    try:
        user = AuthService.get_user_by_google_id(db, google_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        return {
            "tone": user.aury_tone or 'sarcastic',
            "tone_name": {
                'sarcastic': 'Sarcástico',
                'subtle': 'Sutil (Madre Decepcionada)',
                'analytical': 'Analítico'
            }.get(user.aury_tone or 'sarcastic', 'Sarcástico')
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo tono de Aury: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo tono: {str(e)}")

# ==================== FEATURE 9: FREEMIUM (V2.0 - COMENTADO) ====================
# TODO V2.0: Descomentar cuando se implemente modelo Freemium
# @router.get("/user/subscription", response_model=SubscriptionResponse)
# def get_subscription(
#     user_id: UUID,
#     db: Session = Depends(get_db)
# ):
#     """
#     Feature 9: Estado de suscripción del usuario (Freemium)
#     """
#     try:
#         user = db.query(User).filter(User.id == user_id).first()
#         if not user:
#             raise HTTPException(status_code=404, detail="Usuario no encontrado")
#         
#         return SubscriptionResponse(
#             user_id=user_id,
#             is_plus_user=user.is_plus_user,
#             streak_freezes_available=user.streak_freezes_available,
#             has_unlimited_freezes=user.is_plus_user
#         )
#         
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error obteniendo suscripción: {str(e)}")

# ==================== FEATURE 10: PUSH NOTIFICATIONS ====================
@router.post("/notifications/subscribe", response_model=DeviceSubscriptionResponse)
def subscribe_device(
    request: DeviceSubscriptionRequest,
    db: Session = Depends(get_db)
):
    """
    Feature 10: Registrar dispositivo para recibir notificaciones push
    """
    try:
        # Obtener usuario por Google ID
        user = AuthService.get_user_by_google_id(db, request.google_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Verificar si ya existe la suscripción
        existing = db.query(DeviceSubscription)\
            .filter(DeviceSubscription.onesignal_player_id == request.player_id)\
            .first()
        
        if existing:
            # Actualizar si existe
            existing.user_id = user.id
            existing.is_active = True
            existing.device_type = request.device_type
            existing.user_agent = request.user_agent
            db.commit()
            db.refresh(existing)
            
            return DeviceSubscriptionResponse(
                success=True,
                subscription_id=str(existing.id),
                message="Suscripción actualizada"
            )
        else:
            # Crear nueva suscripción
            subscription = DeviceSubscription(
                user_id=user.id,
                onesignal_player_id=request.player_id,
                device_type=request.device_type or "web",
                user_agent=request.user_agent
            )
            db.add(subscription)
            db.commit()
            db.refresh(subscription)
            
            return DeviceSubscriptionResponse(
                success=True,
                subscription_id=str(subscription.id),
                message="Dispositivo suscrito correctamente"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error suscribiendo dispositivo: {e}")
        raise HTTPException(status_code=500, detail=f"Error suscribiendo dispositivo: {str(e)}")

@router.post("/notifications/unsubscribe")
def unsubscribe_device(
    player_id: str,
    google_id: str,
    db: Session = Depends(get_db)
):
    """
    Feature 10: Desactivar suscripción de dispositivo
    """
    try:
        user = AuthService.get_user_by_google_id(db, google_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        subscription = db.query(DeviceSubscription)\
            .filter(
                DeviceSubscription.onesignal_player_id == player_id,
                DeviceSubscription.user_id == user.id
            )\
            .first()
        
        if subscription:
            subscription.is_active = False
            db.commit()
            return {"success": True, "message": "Suscripción desactivada"}
        else:
            raise HTTPException(status_code=404, detail="Suscripción no encontrada")
            
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error desuscribiendo dispositivo: {e}")
        raise HTTPException(status_code=500, detail=f"Error desuscribiendo dispositivo: {str(e)}")
