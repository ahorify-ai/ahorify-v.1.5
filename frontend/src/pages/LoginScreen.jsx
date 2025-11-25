import React, { useEffect, useRef, useState } from 'react';
import api from '../services/api';

export default function LoginScreen({ onLoginSuccess }) {
  const googleButtonRef = useRef(null);
  const [slots, setSlots] = useState(68); // Valor por defecto para generar urgencia

  // Cargar slots restantes de Beta
  useEffect(() => {
    const loadBetaStatus = async () => {
      try {
        const data = await api.getBetaStatus();
        if (data && typeof data.slots_remaining === 'number') {
          // Si hay más de 68 plazas, mostrar 68 para generar urgencia
          // Si hay 68 o menos, mostrar el número real
          const displaySlots = data.slots_remaining > 68 ? 68 : data.slots_remaining;
          setSlots(displaySlots);
        }
      } catch (error) {
        console.error('Error cargando estado de Beta:', error);
        // Mantener 68 por defecto si hay error (para mantener urgencia)
      }
    };

    loadBetaStatus();
  }, []);

  useEffect(() => {
    // Inicializar Google Sign-In cuando el componente se monta
    const initializeGoogleSignIn = () => {
      const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;
      const currentOrigin = window.location.origin;
      
      // Debug: Mostrar información
      console.log('🔍 Debug Google Sign-In:');
      console.log('  - Client ID:', googleClientId ? `${googleClientId.substring(0, 20)}...` : 'NO CONFIGURADO');
      console.log('  - Current Origin:', currentOrigin);
      console.log('  - Expected Origins:', 'http://localhost:3000, http://localhost:5173');
      
      if (!googleClientId) {
        console.error('❌ VITE_GOOGLE_CLIENT_ID no está configurado en .env');
        alert('Error de configuración: VITE_GOOGLE_CLIENT_ID no encontrado. Por favor, verifica el archivo .env');
        return;
      }

      if (window.google && window.google.accounts) {
        try {
          console.log('✅ Inicializando Google Sign-In...');
          window.google.accounts.id.initialize({
            client_id: googleClientId,
            callback: handleGoogleSignIn,
          });

          // Renderizar botón de Google
          if (googleButtonRef.current) {
            console.log('✅ Renderizando botón de Google...');
            window.google.accounts.id.renderButton(
              googleButtonRef.current,
              {
                theme: 'outline',
                size: 'large',
                width: 300,
                text: 'signin_with',
              }
            );
            console.log('✅ Botón de Google renderizado');
          }
        } catch (error) {
          console.error('❌ Error inicializando Google Sign-In:', error);
          console.error('   Detalles:', error.message);
        }
      } else {
        console.warn('⚠️ window.google.accounts no está disponible aún');
      }
    };

    // Esperar a que Google Sign-In esté cargado
    const checkGoogleLoaded = () => {
      if (window.google && window.google.accounts && window.google.accounts.id) {
        console.log('✅ Google Sign-In SDK cargado');
        initializeGoogleSignIn();
      } else {
        console.log('⏳ Esperando a que Google Sign-In SDK se cargue...');
        setTimeout(checkGoogleLoaded, 100);
      }
    };

    // Intentar inicializar inmediatamente
    if (window.google && window.google.accounts && window.google.accounts.id) {
      initializeGoogleSignIn();
    } else {
      // Esperar a que se cargue el script
      window.addEventListener('load', checkGoogleLoaded);
      // También intentar después de un delay
      setTimeout(checkGoogleLoaded, 500);
      return () => window.removeEventListener('load', checkGoogleLoaded);
    }
  }, []);

  const handleGoogleSignIn = async (response) => {
    if (!response || !response.credential) {
      console.error('No se recibió credencial de Google');
      alert('Error: No se recibió credencial de Google. Por favor, intenta de nuevo.');
      return;
    }

    try {
      // Llamar al backend para autenticar
      const result = await api.googleAuth(response.credential);
      
      // Guardar datos del usuario
      localStorage.setItem('google_id', result.google_id);
      localStorage.setItem('email', result.email);
      localStorage.setItem('is_new_user', result.is_new_user);
      
      // Llamar callback de éxito
      onLoginSuccess(result);
    } catch (error) {
      console.error('Error en login:', error);
      const errorMessage = error.message || 'Error desconocido';
      
      if (errorMessage.includes('403') || errorMessage.includes('origin')) {
        alert('Error: El origen http://localhost:3000 no está autorizado en Google Cloud Console.\n\nPor favor, agrega "http://localhost:3000" a los orígenes autorizados en tu proyecto de Google Cloud.');
      } else if (errorMessage.includes('Token') || errorMessage.includes('401')) {
        alert('Error: Token de Google inválido. Por favor, intenta iniciar sesión de nuevo.');
      } else {
        alert(`Error al iniciar sesión: ${errorMessage}`);
      }
    }
  };

  return (
    <div className="min-h-screen bg-white dark:bg-slate-950 text-slate-950 dark:text-white flex flex-col items-center justify-center px-6 relative overflow-hidden">
      {/* Animated Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-50 via-white to-slate-100 dark:from-slate-900 dark:via-slate-950 dark:to-zinc-950 opacity-50"></div>
      <div className="absolute top-20 left-10 w-72 h-72 bg-emerald-500/10 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-orange-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
      
      {/* Content */}
      <div className="relative z-10 max-w-md w-full text-center">
        {/* Logo/Icon */}
        <div className="mb-8 flex justify-center">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-orange-500 to-red-500 opacity-20 blur-2xl rounded-full"></div>
            <div className="relative p-6">
              <img 
                src="/ahorify_icon.png" 
                alt="Ahorify Logo" 
                className="w-20 h-20 object-contain drop-shadow-2xl brightness-110"
              />
            </div>
          </div>
        </div>

        {/* Hero Text */}
        <h1 className="text-5xl md:text-6xl font-bold mb-4 leading-tight">
          <span className="bg-gradient-to-r from-slate-900 via-slate-700 to-slate-500 dark:from-white dark:via-slate-200 dark:to-slate-400 bg-clip-text text-transparent">
            Ahorra o muere
          </span>
          <br />
          <span className="bg-gradient-to-r from-emerald-500 to-emerald-600 dark:from-emerald-400 dark:to-emerald-600 bg-clip-text text-transparent">
            en el intento.
          </span>
        </h1>

        <p className="text-slate-600 dark:text-slate-400 text-lg mb-12 leading-relaxed">
          La primera app de finanzas que no te miente. Aury sí te juzga.
        </p>

        {/* Google Login Button */}
        <div className="w-full mb-4">
          <div ref={googleButtonRef} className="w-full flex justify-center mb-2">
            {/* El botón de Google se renderizará aquí automáticamente */}
          </div>
          <p className="text-slate-700 dark:text-slate-300 text-sm text-center font-medium">
            y Empieza tu Diagnóstico Gratuito
          </p>
        </div>

        {/* Waitlist Scarcity */}
        <div className="inline-flex items-center gap-2 bg-orange-500/10 border border-orange-500/30 rounded-full px-4 py-2">
          <span className="text-orange-500 dark:text-orange-400 text-sm">⚠️</span>
          <span className="text-orange-600 dark:text-orange-300 text-sm font-medium">
            Solo {slots} plazas restantes para la Beta
          </span>
        </div>

        {/* Footer Text */}
        <p className="text-slate-500 dark:text-slate-600 text-xs mt-8">
          Al continuar, aceptas nuestros términos y que te juzguemos sin piedad.
        </p>
      </div>
    </div>
  );
}

