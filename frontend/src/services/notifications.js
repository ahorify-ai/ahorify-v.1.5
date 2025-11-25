// services/notifications.js
import apiClient from './api';

const ONESIGNAL_APP_ID = import.meta.env.VITE_ONESIGNAL_APP_ID;

class NotificationService {
  constructor() {
    this.isInitialized = false;
    this.playerId = null;
    this.OneSignal = null;
  }

  async loadOneSignalSDK() {
    if (window.OneSignal) {
      this.OneSignal = window.OneSignal;
      return;
    }

    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = 'https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js';
      script.async = true;
      script.onload = () => {
        this.OneSignal = window.OneSignal;
        resolve();
      };
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  async initialize(googleId) {
    if (this.isInitialized) {
      return;
    }

    if (!ONESIGNAL_APP_ID) {
      console.warn('⚠️ OneSignal App ID no configurado');
      return;
    }

    try {
      // Cargar SDK de OneSignal
      await this.loadOneSignalSDK();

      // Esperar a que el service worker esté listo (si está disponible)
      if ('serviceWorker' in navigator) {
        try {
          await navigator.serviceWorker.ready;
        } catch (e) {
          // Service worker no disponible, continuar de todas formas
          console.warn('Service Worker no disponible, OneSignal continuará');
        }
      }

      // Inicializar OneSignal
      await this.OneSignal.init({
        appId: ONESIGNAL_APP_ID,
        notifyButton: {
          enable: false, // Ocultamos el botón por defecto, lo manejamos nosotros
        },
        allowLocalhostAsSecureOrigin: true, // Para desarrollo
        serviceWorkerParam: {
          scope: '/',
        },
        serviceWorkerPath: 'OneSignalSDKWorker.js',
      });

      // Obtener Player ID
      const playerId = await this.OneSignal.getUserId();
      
      if (playerId) {
        this.playerId = playerId;
        await this.subscribeDevice(googleId, playerId);
      } else {
        // Esperar a que OneSignal genere el Player ID
        this.OneSignal.on('subscriptionChange', async (isSubscribed) => {
          if (isSubscribed) {
            const newPlayerId = await this.OneSignal.getUserId();
            if (newPlayerId) {
              this.playerId = newPlayerId;
              await this.subscribeDevice(googleId, newPlayerId);
            }
          }
        });
      }

      this.isInitialized = true;
      console.log('✅ OneSignal inicializado correctamente');
    } catch (error) {
      console.error('❌ Error inicializando OneSignal:', error);
    }
  }

  async subscribeDevice(googleId, playerId) {
    try {
      const userAgent = navigator.userAgent;
      const deviceType = this.getDeviceType();

      await apiClient.request('/api/v1/notifications/subscribe', {
        method: 'POST',
        body: {
          google_id: googleId,
          player_id: playerId,
          device_type: deviceType,
          user_agent: userAgent,
        },
      });

      console.log('✅ Dispositivo suscrito para notificaciones');
    } catch (error) {
      console.error('❌ Error suscribiendo dispositivo:', error);
    }
  }

  async requestPermission() {
    try {
      if (!this.OneSignal) {
        await this.loadOneSignalSDK();
        if (!ONESIGNAL_APP_ID) {
          console.warn('⚠️ OneSignal App ID no configurado');
          return false;
        }
        await this.OneSignal.init({
          appId: ONESIGNAL_APP_ID,
          allowLocalhostAsSecureOrigin: true,
        });
      }

      const permission = await this.OneSignal.registerForPushNotifications();
      return permission;
    } catch (error) {
      console.error('❌ Error solicitando permiso:', error);
      return false;
    }
  }

  async isSubscribed() {
    try {
      if (!this.OneSignal) {
        return false;
      }
      return await this.OneSignal.isPushNotificationsEnabled();
    } catch (error) {
      console.error('❌ Error verificando suscripción:', error);
      return false;
    }
  }

  getDeviceType() {
    const ua = navigator.userAgent;
    if (/iPhone|iPad|iPod/.test(ua)) return 'ios';
    if (/Android/.test(ua)) return 'android';
    return 'web';
  }

  async unsubscribe(googleId) {
    try {
      if (this.playerId && this.OneSignal) {
        await apiClient.request(
          `/api/v1/notifications/unsubscribe?player_id=${this.playerId}&google_id=${googleId}`,
          { method: 'POST' }
        );
        await this.OneSignal.setSubscription(false);
        console.log('✅ Notificaciones desactivadas');
      }
    } catch (error) {
      console.error('❌ Error desuscribiendo:', error);
    }
  }
}

export default new NotificationService();

