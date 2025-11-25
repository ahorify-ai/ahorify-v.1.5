#!/usr/bin/env python3
"""
Script para enviar recordatorios diarios de racha
Ejecutar con cron diariamente (ej: 20:00)
"""

import sys
import os
from datetime import date, timedelta

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models import User, Streak
from api.v1.services.notification_service import NotificationService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_daily_reminders():
    """Envía recordatorios diarios a usuarios activos"""
    db: Session = SessionLocal()
    
    try:
        # Obtener usuarios con racha activa
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        # Usuarios que tienen racha y su última actividad fue ayer o antes
        users_to_remind = db.query(User)\
            .join(Streak)\
            .filter(
                Streak.current_streak > 0,
                Streak.last_activity_date <= yesterday
            )\
            .all()
        
        logger.info(f"Enviando recordatorios a {len(users_to_remind)} usuarios")
        
        for user in users_to_remind:
            streak = db.query(Streak).filter(Streak.user_id == user.id).first()
            
            # Si la última actividad fue ayer, está en riesgo
            if streak.last_activity_date == yesterday:
                NotificationService.send_streak_risk_alert(db, user)
            else:
                # Recordatorio normal
                NotificationService.send_streak_reminder(db, user)
        
        logger.info("✅ Recordatorios enviados correctamente")
        
    except Exception as e:
        logger.error(f"❌ Error enviando recordatorios: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    send_daily_reminders()

