// src/pages/SettingsScreen.jsx
import React, { useState, useEffect } from 'react';
import { ArrowLeft, Settings as SettingsIcon, Download, Smartphone, LogOut } from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';
import NotificationSettings from '../components/NotificationSettings';
import api from '../services/api';

export default function SettingsScreen({ onBack, onLogout }) {
  const { theme, toggleTheme } = useTheme();
  const [auryTone, setAuryTone] = useState('sarcastic');
  const [loading, setLoading] = useState(false);
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [isInstalled, setIsInstalled] = useState(false);
  const [isIOS, setIsIOS] = useState(false);
  const [isAndroid, setIsAndroid] = useState(false);
  const googleId = localStorage.getItem('google_id');

  useEffect(() => {
    loadAuryTone();
    checkInstallStatus();
    detectDevice();
    
    // Escuchar evento beforeinstallprompt (Android)
    const handleBeforeInstallPrompt = (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
    };
    
    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    
    // Detectar si la app ya está instalada
    if (window.matchMedia('(display-mode: standalone)').matches) {
      setIsInstalled(true);
    }
    
    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    };
  }, []);
  
  const checkInstallStatus = () => {
    // Verificar si está en modo standalone (instalada)
    if (window.matchMedia('(display-mode: standalone)').matches) {
      setIsInstalled(true);
    }
    
    // Verificar si está en modo standalone en iOS
    if (window.navigator.standalone === true) {
      setIsInstalled(true);
    }
  };
  
  const detectDevice = () => {
    const userAgent = window.navigator.userAgent.toLowerCase();
    const isIOSDevice = /iphone|ipad|ipod/.test(userAgent);
    const isAndroidDevice = /android/.test(userAgent);
    
    setIsIOS(isIOSDevice);
    setIsAndroid(isAndroidDevice);
  };
  
  const handleInstallClick = async () => {
    if (!deferredPrompt) return;
    
    // Mostrar el prompt de instalación
    deferredPrompt.prompt();
    
    // Esperar a que el usuario responda
    const { outcome } = await deferredPrompt.userChoice;
    
    if (outcome === 'accepted') {
      console.log('Usuario aceptó instalar la app');
    } else {
      console.log('Usuario rechazó instalar la app');
    }
    
    // Limpiar el prompt
    setDeferredPrompt(null);
  };

  const loadAuryTone = async () => {
    if (!googleId) return;
    try {
      const data = await api.getAuryTone(googleId);
      setAuryTone(data.tone || 'sarcastic');
    } catch (error) {
      console.error('Error cargando tono de Aury:', error);
    }
  };

  const handleAuryToneChange = async (newTone) => {
    if (!googleId || loading) return;
    setLoading(true);
    try {
      await api.setAuryTone(googleId, newTone);
      setAuryTone(newTone);
    } catch (error) {
      console.error('Error cambiando tono:', error);
      alert('Error al cambiar el tono. Por favor, intenta de nuevo.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    if (window.confirm('¿Estás seguro de que quieres cerrar sesión?')) {
      if (onLogout) {
        onLogout();
      }
    }
  };

  const toneOptions = [
    { value: 'sarcastic', label: 'Sarcástica', description: 'Tono cínico y condescendiente (Default)' },
    { value: 'subtle', label: 'Decepcionada', description: 'Tono melancólico, como una madre decepcionada' },
    { value: 'analytical', label: 'Analista Fría', description: 'Tono objetivo, basado en datos y porcentajes' },
  ];

  const themeOptions = [
    { value: 'system', label: 'Sistema', description: 'Usar preferencia del sistema' },
    { value: 'light', label: 'Claro', description: 'Tema claro' },
    { value: 'dark', label: 'Oscuro', description: 'Tema oscuro' },
  ];

  return (
    <div className="min-h-screen bg-white dark:bg-slate-950 text-slate-950 dark:text-white flex flex-col">
      {/* Header */}
      <header className="px-6 py-4 flex items-center gap-4 border-b border-slate-200 dark:border-slate-800">
        <button
          onClick={onBack}
          className="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full transition-colors"
        >
          <ArrowLeft size={20} />
        </button>
        <div className="flex items-center gap-2">
          <SettingsIcon size={20} />
          <h1 className="text-xl font-semibold">Configuración</h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 px-6 py-6 overflow-y-auto">
        <div className="max-w-2xl mx-auto space-y-6">
          
          {/* 1. Tono de Aury */}
          <section className="bg-slate-50 dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              🗣️ Tono del Agente Aury
            </h2>
            <p className="text-sm text-slate-600 dark:text-slate-400 mb-4">
              Elige cómo quieres que Aury te hable. Cada tono tiene un enfoque diferente para motivarte.
            </p>
            <div className="space-y-3">
              {toneOptions.map((option) => (
                <label
                  key={option.value}
                  className={`flex items-start gap-3 p-4 rounded-xl border-2 cursor-pointer transition-all ${
                    auryTone === option.value
                      ? 'border-emerald-500 bg-emerald-50 dark:bg-emerald-900/20'
                      : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600'
                  }`}
                >
                  <input
                    type="radio"
                    name="auryTone"
                    value={option.value}
                    checked={auryTone === option.value}
                    onChange={() => handleAuryToneChange(option.value)}
                    disabled={loading}
                    className="mt-1"
                  />
                  <div className="flex-1">
                    <div className="font-medium">{option.label}</div>
                    <div className="text-sm text-slate-600 dark:text-slate-400 mt-1">
                      {option.description}
                    </div>
                  </div>
                </label>
              ))}
            </div>
          </section>

          {/* 2. Preferencias de Notificación */}
          <section className="bg-slate-50 dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              🔔 Preferencias de Notificación
            </h2>
            <NotificationSettings googleId={googleId} />
          </section>

          {/* 3. Apariencia */}
          <section className="bg-slate-50 dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              📱 Apariencia
            </h2>
            <p className="text-sm text-slate-600 dark:text-slate-400 mb-4">
              Personaliza la apariencia de la aplicación según tu preferencia.
            </p>
            <div className="space-y-3">
              {themeOptions.map((option) => (
                <label
                  key={option.value}
                  className={`flex items-start gap-3 p-4 rounded-xl border-2 cursor-pointer transition-all ${
                    theme === option.value
                      ? 'border-emerald-500 bg-emerald-50 dark:bg-emerald-900/20'
                      : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600'
                  }`}
                >
                  <input
                    type="radio"
                    name="theme"
                    value={option.value}
                    checked={theme === option.value}
                    onChange={() => toggleTheme(option.value)}
                    className="mt-1"
                  />
                  <div className="flex-1">
                    <div className="font-medium">{option.label}</div>
                    <div className="text-sm text-slate-600 dark:text-slate-400 mt-1">
                      {option.description}
                    </div>
                  </div>
                </label>
              ))}
            </div>
          </section>

          {/* 4. Instalar App */}
          {!isInstalled && (
            <section className="bg-slate-50 dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Smartphone size={20} />
                Añadir a la Pantalla de Inicio
              </h2>
              <p className="text-sm text-slate-600 dark:text-slate-400 mb-4">
                Instala Ahorify en tu dispositivo para acceder más rápido y tener una mejor experiencia.
              </p>
              
              {/* Botón de instalación automática (Android) */}
              {deferredPrompt && isAndroid && (
                <button
                  onClick={handleInstallClick}
                  className="w-full bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-400 hover:to-emerald-500 text-white font-semibold py-3 px-6 rounded-xl flex items-center justify-center gap-2 transition-all transform hover:scale-105 active:scale-95 mb-4"
                >
                  <Download size={20} />
                  Instalar Ahorify
                </button>
              )}
              
              {/* Instrucciones para iOS */}
              {isIOS && (
                <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-4 mb-4">
                  <h3 className="font-semibold text-blue-900 dark:text-blue-100 mb-2 flex items-center gap-2">
                    📱 Instrucciones para iOS (Safari)
                  </h3>
                  <ol className="text-sm text-blue-800 dark:text-blue-200 space-y-2 list-decimal list-inside">
                    <li>Toca el botón <strong>Compartir</strong> (□↑) en la parte inferior</li>
                    <li>Desplázate y selecciona <strong>"Añadir a pantalla de inicio"</strong></li>
                    <li>Toca <strong>"Añadir"</strong> para confirmar</li>
                    <li>¡Listo! Ahorify aparecerá en tu pantalla de inicio</li>
                  </ol>
                </div>
              )}
              
              {/* Instrucciones para Android (si no hay prompt automático) */}
              {isAndroid && !deferredPrompt && (
                <div className="bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-xl p-4">
                  <h3 className="font-semibold text-emerald-900 dark:text-emerald-100 mb-2 flex items-center gap-2">
                    🤖 Instrucciones para Android
                  </h3>
                  <ol className="text-sm text-emerald-800 dark:text-emerald-200 space-y-2 list-decimal list-inside">
                    <li>Toca el menú (⋮) en la esquina superior derecha</li>
                    <li>Selecciona <strong>"Añadir a la pantalla de inicio"</strong> o <strong>"Instalar app"</strong></li>
                    <li>Confirma la instalación</li>
                    <li>¡Listo! Ahorify aparecerá en tu pantalla de inicio</li>
                  </ol>
                </div>
              )}
              
              {/* Instrucciones genéricas si no se detecta dispositivo */}
              {!isIOS && !isAndroid && (
                <div className="bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl p-4">
                  <h3 className="font-semibold mb-2">📱 Instrucciones</h3>
                  <p className="text-sm text-slate-600 dark:text-slate-400 mb-2">
                    Busca la opción <strong>"Añadir a la pantalla de inicio"</strong> o <strong>"Instalar app"</strong> en el menú de tu navegador.
                  </p>
                  <p className="text-xs text-slate-500 dark:text-slate-500">
                    Esta función está disponible en navegadores móviles modernos.
                  </p>
                </div>
              )}
            </section>
          )}
          
          {/* Mensaje si ya está instalada */}
          {isInstalled && (
            <section className="bg-emerald-50 dark:bg-emerald-900/20 rounded-2xl p-6 border border-emerald-200 dark:border-emerald-800">
              <div className="flex items-center gap-3">
                <div className="bg-emerald-500 rounded-full p-2">
                  <Smartphone size={20} className="text-white" />
                </div>
                <div>
                  <h3 className="font-semibold text-emerald-900 dark:text-emerald-100">
                    ✅ Ahorify está instalada
                  </h3>
                  <p className="text-sm text-emerald-700 dark:text-emerald-300 mt-1">
                    La aplicación está instalada en tu dispositivo.
                  </p>
                </div>
              </div>
            </section>
          )}

          {/* 5. Cerrar Sesión */}
          <section className="bg-red-50 dark:bg-red-900/20 rounded-2xl p-6 border border-red-200 dark:border-red-800">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2 text-red-700 dark:text-red-300">
              <LogOut size={20} />
              Cerrar Sesión
            </h2>
            <p className="text-sm text-red-600 dark:text-red-400 mb-4">
              Cierra tu sesión para cambiar de cuenta o salir de la aplicación.
            </p>
            <button
              onClick={handleLogout}
              className="w-full bg-red-500 hover:bg-red-600 text-white font-semibold py-3 px-6 rounded-xl flex items-center justify-center gap-2 transition-all transform hover:scale-105 active:scale-95"
            >
              <LogOut size={20} />
              Cerrar Sesión
            </button>
          </section>

        </div>
      </main>
    </div>
  );
}

