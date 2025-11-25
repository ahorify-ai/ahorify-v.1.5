// API Client para conectar con FastAPI Backend
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // Si hay body, convertir a JSON
    if (config.body && typeof config.body === 'object') {
      config.body = JSON.stringify(config.body);
    }

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Error en la petición' }));
        throw new Error(error.detail || `Error ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // Feature 1: Google Auth
  async googleAuth(token) {
    return this.request('/api/v1/auth/google', {
      method: 'POST',
      body: { token },
    });
  }

  // Feature 4, 5, 7: Crear gasto
  async crearGasto(rawText, googleId) {
    return this.request('/api/v1/gasto', {
      method: 'POST',
      body: { 
        raw_text: rawText, 
        google_id: googleId 
      },
    });
  }

  // Feature 6, 8: Obtener racha
  async getRacha(googleId) {
    return this.request(`/api/v1/racha?google_id=${googleId}`);
  }

  // Feature 7: Feed de gastos
  async getGastos(googleId, limit = 20) {
    return this.request(`/api/v1/gastos/recent?google_id=${googleId}&limit=${limit}`);
  }

  // Feature 8: Usar freeze
  async usarFreeze(googleId) {
    return this.request('/api/v1/streak/freeze', {
      method: 'POST',
      body: { google_id: googleId },
    });
  }

  // Feature 3: Guardar objetivo
  async setGoal(googleId, goal) {
    return this.request(`/api/v1/user/goal?google_id=${googleId}`, {
      method: 'POST',
      body: { goal },
    });
  }

  // Feature 2: Waitlist status
  async getWaitlistStatus() {
    return this.request('/api/v1/waitlist/status');
  }

  // Public: Beta status (slots restantes)
  async getBetaStatus() {
    return this.request('/api/v1/public/beta-status');
  }

  // Feature 10: Notificaciones
  async subscribeDevice(googleId, playerId, deviceType = 'web', userAgent = null) {
    return this.request('/api/v1/notifications/subscribe', {
      method: 'POST',
      body: {
        google_id: googleId,
        player_id: playerId,
        device_type: deviceType,
        user_agent: userAgent,
      },
    });
  }

  async unsubscribeDevice(googleId, playerId) {
    return this.request(
      `/api/v1/notifications/unsubscribe?player_id=${playerId}&google_id=${googleId}`,
      { method: 'POST' }
    );
  }

  // Aury Tone
  async getAuryTone(googleId) {
    return this.request(`/api/v1/user/aury-tone?google_id=${googleId}`);
  }

  async setAuryTone(googleId, tone) {
    return this.request('/api/v1/user/aury-tone', {
      method: 'POST',
      body: {
        google_id: googleId,
        tone: tone,
      },
    });
  }
}

export default new ApiClient();

