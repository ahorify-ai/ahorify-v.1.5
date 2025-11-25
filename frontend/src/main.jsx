import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

// Registrar Service Worker para PWA (VitePWA lo maneja automáticamente)
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    // VitePWA registra el service worker automáticamente
    // Verificar que esté disponible
    navigator.serviceWorker.ready.then((registration) => {
      if (import.meta.env.DEV) {
        console.log('✅ Service Worker registrado (desarrollo)');
      } else {
        console.log('✅ Service Worker registrado (producción)');
      }
    }).catch((error) => {
      console.warn('⚠️ Service Worker no disponible:', error);
    });
  });
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)

