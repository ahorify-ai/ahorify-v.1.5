# api/v1/services/notification_service.py
"""
Notification Service - Feature 10
Gestiona el envío de notificaciones push mediante OneSignal
"""

import requests
import logging
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from datetime import datetime, time

from api.config import ONESIGNAL_APP_ID, ONESIGNAL_REST_API_KEY
from api.models import User, DeviceSubscription, Streak

logger = logging.getLogger(__name__)

class NotificationService:
    """Servicio para gestionar notificaciones push con OneSignal"""
    
    ONESIGNAL_API_URL = "https://onesignal.com/api/v1/notifications"
    
    @staticmethod
    def send_notification(
        player_ids: List[str],
        heading: str,
        message: str,
        data: Optional[Dict] = None,
        url: Optional[str] = None
    ) -> bool:
        """
        Envía notificación push a través de OneSignal
        
        Args:
            player_ids: Lista de OneSignal Player IDs
            heading: Título de la notificación
            message: Mensaje de la notificación
            data: Datos adicionales (opcional)
            url: URL a abrir al hacer click (opcional)
            
        Returns:
            True si se envió correctamente, False en caso contrario
        """
        if not ONESIGNAL_APP_ID or not ONESIGNAL_REST_API_KEY:
            logger.warning("OneSignal no configurado. Saltando envío de notificación.")
            return False
        
        if not player_ids:
            logger.warning("No hay player_ids para enviar notificación.")
            return False
        
        payload = {
            "app_id": ONESIGNAL_APP_ID,
            "include_player_ids": player_ids,
            "headings": {"en": heading, "es": heading},
            "contents": {"en": message, "es": message},
        }
        
        if data:
            payload["data"] = data
        
        if url:
            payload["url"] = url
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {ONESIGNAL_REST_API_KEY}"
        }
        
        try:
            response = requests.post(
                NotificationService.ONESIGNAL_API_URL,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            logger.info(f"Notificación enviada exitosamente a {len(player_ids)} dispositivos")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Error enviando notificación OneSignal: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.text}")
            return False
    
    @staticmethod
    def send_streak_reminder(db: Session, user: User) -> bool:
        """
        Envía recordatorio diario de racha al usuario
        """
        # Obtener suscripciones activas del usuario
        subscriptions = db.query(DeviceSubscription)\
            .filter(
                DeviceSubscription.user_id == user.id,
                DeviceSubscription.is_active == True
            )\
            .all()
        
        if not subscriptions:
            logger.info(f"Usuario {user.id} no tiene dispositivos suscritos")
            return False
        
        player_ids = [sub.onesignal_player_id for sub in subscriptions]
        
        # Obtener información de racha
        streak = db.query(Streak).filter(Streak.user_id == user.id).first()
        current_streak = streak.current_streak if streak else 0
        
        heading = "🔥 ¡No rompas tu racha!"
        message = f"Llevas {current_streak} días consecutivos. ¡Registra un gasto hoy para mantenerla!"
        
        return NotificationService.send_notification(
            player_ids=player_ids,
            heading=heading,
            message=message,
            data={"type": "streak_reminder", "user_id": str(user.id)},
            url="/dashboard"
        )
    
    @staticmethod
    def send_streak_risk_alert(db: Session, user: User) -> bool:
        """
        Envía alerta cuando la racha está en riesgo (último día sin actividad)
        """
        subscriptions = db.query(DeviceSubscription)\
            .filter(
                DeviceSubscription.user_id == user.id,
                DeviceSubscription.is_active == True
            )\
            .all()
        
        if not subscriptions:
            return False
        
        player_ids = [sub.onesignal_player_id for sub in subscriptions]
        
        streak = db.query(Streak).filter(Streak.user_id == user.id).first()
        current_streak = streak.current_streak if streak else 0
        
        heading = "⚠️ ¡Tu racha está en peligro!"
        message = f"Tienes {current_streak} días de racha. ¡Registra un gasto ahora o la perderás!"
        
        return NotificationService.send_notification(
            player_ids=player_ids,
            heading=heading,
            message=message,
            data={"type": "streak_risk", "user_id": str(user.id)},
            url="/dashboard"
        )
    
    @staticmethod
    def send_streak_milestone(db: Session, user: User, milestone_days: int) -> bool:
        """
        Envía notificación de hito de racha (ej: 7 días, 30 días)
        """
        subscriptions = db.query(DeviceSubscription)\
            .filter(
                DeviceSubscription.user_id == user.id,
                DeviceSubscription.is_active == True
            )\
            .all()
        
        if not subscriptions:
            return False
        
        player_ids = [sub.onesignal_player_id for sub in subscriptions]
        
        heading = "🎉 ¡Hito alcanzado!"
        message = f"¡Felicidades! Has alcanzado {milestone_days} días consecutivos de racha. ¡Sigue así!"
        
        return NotificationService.send_notification(
            player_ids=player_ids,
            heading=heading,
            message=message,
            data={"type": "streak_milestone", "user_id": str(user.id), "days": milestone_days},
            url="/dashboard"
        )

