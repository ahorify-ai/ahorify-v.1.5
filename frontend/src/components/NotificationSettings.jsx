// components/NotificationSettings.jsx
import React, { useState, useEffect } from 'react';
import notificationService from '../services/notifications';

/**
 * Componente opcional para gestionar preferencias de notificaciones
 * Puede ser usado en el Dashboard o en una pantalla de configuración
 */
function NotificationSettings({ googleId }) {
  const [isSubscribed, setIsSubscribed] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    checkSubscriptionStatus();
  }, []);

  const checkSubscriptionStatus = async () => {
    try {
      setIsLoading(true);
      const subscribed = await notificationService.isSubscribed();
      setIsSubscribed(subscribed);
      setError(null);
    } catch (err) {
      console.error('Error verificando suscripción:', err);
      setError('No se pudo verificar el estado de las notificaciones');
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggleNotifications = async () => {
    try {
      setIsLoading(true);
      setError(null);

      if (isSubscribed) {
        // Desactivar notificaciones
        await notificationService.unsubscribe(googleId);
        setIsSubscribed(false);
      } else {
        // Activar notificaciones
        const permission = await notificationService.requestPermission();
        if (permission) {
          // Re-inicializar para obtener el nuevo Player ID
          await notificationService.initialize(googleId);
          setIsSubscribed(true);
        } else {
          setError('Permisos de notificaciones denegados');
        }
      }
    } catch (err) {
      console.error('Error cambiando suscripción:', err);
      setError('No se pudo cambiar el estado de las notificaciones');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="p-4 bg-slate-100 dark:bg-slate-800 rounded-lg">
        <p className="text-slate-600 dark:text-slate-400">Verificando estado de notificaciones...</p>
      </div>
    );
  }

  return (
    <div>
      {error && (
        <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded text-red-700 dark:text-red-400 text-sm">
          {error}
        </div>
      )}

      <div className="flex items-center justify-between">
        <div>
          <p className="font-medium text-slate-900 dark:text-slate-100">
            {isSubscribed ? 'Notificaciones activadas' : 'Notificaciones desactivadas'}
          </p>
          <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
            {isSubscribed
              ? 'Recibirás recordatorios diarios de tu racha'
              : 'Activa las notificaciones para recibir recordatorios'}
          </p>
        </div>
        
        <button
          onClick={handleToggleNotifications}
          disabled={isLoading}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            isSubscribed
              ? 'bg-red-500 hover:bg-red-600 text-white'
              : 'bg-emerald-500 hover:bg-emerald-600 text-white'
          } disabled:opacity-50 disabled:cursor-not-allowed`}
        >
          {isSubscribed ? 'Desactivar' : 'Activar'}
        </button>
      </div>
    </div>
  );
}

export default NotificationSettings;

