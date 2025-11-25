# api/v1/services/streak_service.py
"""
Streak Service - Feature 6, 8
Lógica de rachas resiliente con Freeze (Vidas Extra)
V1.5: Protector semanal gratuito (1 uso por semana)
"""

from datetime import date, timedelta
from typing import Dict, Optional
from sqlalchemy.orm import Session
from api.models import Streak, User
import logging

logger = logging.getLogger(__name__)

class StreakService:
    """
    Feature 8: Lógica de racha resiliente con Streak Freeze
    """
    
    @staticmethod
    def get_or_create_streak(db: Session, user_id) -> Streak:
        """Obtiene o crea el streak del usuario"""
        streak = db.query(Streak).filter(Streak.user_id == user_id).first()
        if not streak:
            streak = Streak(user_id=user_id, current_streak=0, longest_streak=0)
            db.add(streak)
            db.commit()
            db.refresh(streak)
        return streak
    
    @staticmethod
    def update_streak(db: Session, user_id, activity_date: date = None) -> Dict:
        """
        Feature 8: Actualiza la racha del usuario
        Lógica resiliente: verifica días consecutivos y maneja breaks
        """
        if activity_date is None:
            activity_date = date.today()
        
        streak = StreakService.get_or_create_streak(db, user_id)
        user = db.query(User).filter(User.id == user_id).first()
        
        if not streak.last_activity_date:
            # Primera actividad - iniciar racha
            streak.current_streak = 1
            streak.longest_streak = 1
            streak.last_activity_date = activity_date
            db.commit()
            return {
                "streak_updated": True,
                "current_streak": 1,
                "message": "🎉 ¡Comienza tu racha financiera!"
            }
        
        days_since_last = (activity_date - streak.last_activity_date).days
        
        if days_since_last == 0:
            # Ya activo hoy - mantener racha
            return {
                "streak_updated": False,
                "current_streak": streak.current_streak,
                "message": "Racha mantenida - ya activo hoy"
            }
        elif days_since_last == 1:
            # Día consecutivo - incrementar racha
            new_streak = streak.current_streak + 1
            longest_streak = max(streak.longest_streak, new_streak)
            
            streak.current_streak = new_streak
            streak.longest_streak = longest_streak
            streak.last_activity_date = activity_date
            db.commit()
            
            return {
                "streak_updated": True,
                "current_streak": new_streak,
                "message": f"🔥 ¡Racha de {new_streak} días!"
            }
        else:
            # Break en la racha - Feature 8: Verificar si tiene vidas
            return StreakService._handle_streak_break(db, streak, user, activity_date, days_since_last)
    
    @staticmethod
    def _handle_streak_break(db: Session, streak: Streak, user: User, activity_date: date, days_since_last: int) -> Dict:
        """
        Feature 8: Maneja la ruptura de racha con lógica de Freeze semanal
        V1.5: Todos los usuarios tienen 1 protector gratis por semana
        Si pierden la racha 2 veces en una semana, la racha vuelve a cero
        """
        # V1.5: Resetear contador semanal si es nueva semana
        StreakService._reset_weekly_counter_if_new_week(db, user, activity_date)
        
        # V1.5: Verificar si puede usar el protector semanal
        can_use_weekly_freeze = StreakService._can_use_weekly_freeze(user, activity_date)
        
        # TODO V2.0: Agregar lógica PLUS
        # if user.is_plus_user:
        #     # Usuarios PLUS tienen protección ilimitada
        #     streak.last_activity_date = activity_date
        #     db.commit()
        #     return {"streak_updated": False, "current_streak": streak.current_streak, "message": "🛡️ Racha protegida (Plus)"}
        
        if can_use_weekly_freeze:
            # Usar protector semanal
            user.last_weekly_freeze_date = activity_date
            user.weekly_freeze_count += 1
            streak.last_activity_date = activity_date
            db.commit()
            
            return {
                "streak_updated": False,  # No incrementa, solo mantiene
                "current_streak": streak.current_streak,
                "freeze_used": True,
                "weekly_freeze_used": True,
                "message": f"🛡️ Racha protegida con protector semanal ({user.weekly_freeze_count}/1 esta semana)"
            }
        elif user.weekly_freeze_count >= 1:
            # Ya usó el protector esta semana, segunda pérdida = racha a cero
            streak.current_streak = 0  # Reiniciar a cero (no a 1)
            streak.longest_streak = max(streak.longest_streak, streak.current_streak)
            streak.last_activity_date = activity_date
            # Resetear contador semanal para próxima semana
            user.weekly_freeze_count = 0
            user.last_weekly_freeze_date = None
            db.commit()
            
            return {
                "streak_updated": True,
                "current_streak": 0,
                "message": f"💔 Racha perdida dos veces esta semana. Racha reiniciada a 0."
            }
        else:
            # Primera pérdida de la semana, pero ya no tiene protector (o nunca lo tuvo)
            streak.current_streak = 1  # Reiniciar
            streak.longest_streak = max(streak.longest_streak, streak.current_streak)
            streak.last_activity_date = activity_date
            db.commit()
            
            return {
                "streak_updated": True,
                "current_streak": 1,
                "message": f"💔 Racha rota. Nueva racha iniciada."
            }
    
    @staticmethod
    def _can_use_weekly_freeze(user: User, current_date: date) -> bool:
        """
        V1.5: Verifica si el usuario puede usar el protector semanal
        Reglas:
        - 1 protector gratis por semana
        - Si no ha usado ninguno esta semana, puede usarlo
        - Las semanas se resetean cada lunes
        """
        if user.last_weekly_freeze_date is None:
            # Nunca ha usado el protector, puede usarlo
            return True
        
        # Calcular si estamos en la misma semana
        # Una semana va de lunes a domingo (ISO week)
        last_freeze_week = StreakService._get_week_number(user.last_weekly_freeze_date)
        current_week = StreakService._get_week_number(current_date)
        
        if current_week > last_freeze_week:
            # Nueva semana, puede usar (contador se reseteará cuando lo use)
            return True
        
        if current_week == last_freeze_week:
            # Misma semana
            if user.weekly_freeze_count == 0:
                # Contador ya reseteado, puede usar
                return True
            else:
                # Ya usó el protector esta semana
                return False
        
        # No debería llegar aquí, pero por seguridad
        return False
    
    @staticmethod
    def can_use_weekly_freeze(db: Session, user: User, current_date: date) -> bool:
        """
        Versión pública que también resetea el contador si es nueva semana
        """
        # Resetear contador si es nueva semana
        StreakService._reset_weekly_counter_if_new_week(db, user, current_date)
        return StreakService._can_use_weekly_freeze(user, current_date)
    
    @staticmethod
    def _get_week_number(d: date) -> int:
        """
        Obtiene el número de semana del año (formato ISO: año-semana)
        Retorna un entero único para cada semana
        """
        # ISO week: año * 100 + semana
        iso_year, iso_week, _ = d.isocalendar()
        return iso_year * 100 + iso_week
    
    @staticmethod
    def _reset_weekly_counter_if_new_week(db: Session, user: User, current_date: date):
        """
        V1.5: Resetea el contador semanal si estamos en una nueva semana
        """
        if user.last_weekly_freeze_date is None:
            return
        
        last_freeze_week = StreakService._get_week_number(user.last_weekly_freeze_date)
        current_week = StreakService._get_week_number(current_date)
        
        if current_week > last_freeze_week:
            # Nueva semana, resetear contador
            user.weekly_freeze_count = 0
            user.last_weekly_freeze_date = None
            db.commit()
    
    @staticmethod
    def use_freeze(db: Session, user_id) -> Dict:
        """
        Feature 8: Usar protector semanal manualmente
        V1.5: Protector semanal gratuito (1 por semana)
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"success": False, "message": "Usuario no encontrado"}
        
        # TODO V2.0: Agregar lógica PLUS
        # if user.is_plus_user:
        #     return {
        #         "success": True,
        #         "freeze_used": False,
        #         "remaining_freezes": -1,  # Ilimitado
        #         "message": "Tienes protección ilimitada (Plus)"
        #     }
        
        # V1.5: Verificar si puede usar el protector semanal
        current_date = date.today()
        can_use = StreakService.can_use_weekly_freeze(db, user, current_date)
        
        if not can_use:
            return {
                "success": False,
                "freeze_used": False,
                "remaining_freezes": 0,
                "message": f"Ya usaste tu protector semanal ({user.weekly_freeze_count}/1 esta semana). Resetea el lunes."
            }
        
        # Usar protector semanal
        user.last_weekly_freeze_date = current_date
        user.weekly_freeze_count = 1
        db.commit()
        
        return {
            "success": True,
            "freeze_used": True,
            "remaining_freezes": 1 - user.weekly_freeze_count,
            "message": f"Protector semanal usado. Ya no puedes usar otro hasta el próximo lunes."
        }

