import React, { useState, useEffect } from 'react';
import LoginScreen from './pages/LoginScreen';
import GoalScreen from './pages/GoalScreen';
import Dashboard from './pages/Dashboard';
import SettingsScreen from './pages/SettingsScreen';
import { ThemeProvider } from './contexts/ThemeContext';
import notificationService from './services/notifications';

function App() {
  const [currentScreen, setCurrentScreen] = useState('login'); // 'login' | 'goal' | 'dashboard'
  const [userData, setUserData] = useState({
    googleId: null,
    email: null,
    userName: null,
    goal: null,
    isNewUser: false,
  });

  // Verificar si hay sesión guardada al cargar
  useEffect(() => {
    const googleId = localStorage.getItem('google_id');
    const email = localStorage.getItem('email');
    const goal = localStorage.getItem('user_goal');
    const isNewUser = localStorage.getItem('is_new_user') === 'true';

    if (googleId && email) {
      // Extraer nombre del email (antes del @)
      const userName = email.split('@')[0];
      
      setUserData({
        googleId,
        email,
        userName,
        goal,
        isNewUser,
      });

      // Inicializar notificaciones cuando hay usuario logueado
      if (googleId) {
        notificationService.initialize(googleId);
      }

      // Si no tiene goal, mostrar pantalla de goal
      if (!goal) {
        setCurrentScreen('goal');
      } else {
        setCurrentScreen('dashboard');
      }
    }
  }, []);

  const handleLoginSuccess = async (result) => {
    const userName = result.email.split('@')[0];
    
    setUserData({
      googleId: result.google_id,
      email: result.email,
      userName,
      goal: null,
      isNewUser: result.is_new_user,
    });

    // Inicializar notificaciones después del login
    await notificationService.initialize(result.google_id);
    
    // Solicitar permiso de notificaciones después de un breve delay
    setTimeout(async () => {
      const hasPermission = await notificationService.isSubscribed();
      if (!hasPermission) {
        await notificationService.requestPermission();
      }
    }, 1000);

    // Si es usuario nuevo o no tiene goal, mostrar pantalla de goal
    if (result.is_new_user || !localStorage.getItem('user_goal')) {
      setCurrentScreen('goal');
    } else {
      setCurrentScreen('dashboard');
    }
  };

  const handleGoalSet = (goal) => {
    // Guardar goal en localStorage
    localStorage.setItem('user_goal', goal);
    
    setUserData(prev => ({
      ...prev,
      goal,
    }));

    // Ir al dashboard
    setCurrentScreen('dashboard');
  };

  const handleLogout = () => {
    // Limpiar datos de sesión del localStorage
    localStorage.removeItem('google_id');
    localStorage.removeItem('email');
    localStorage.removeItem('user_goal');
    localStorage.removeItem('is_new_user');
    
    // Resetear estado
    setUserData({
      googleId: null,
      email: null,
      userName: null,
      goal: null,
      isNewUser: false,
    });
    
    // Volver a la pantalla de login
    setCurrentScreen('login');
  };

  // Renderizar pantalla actual
  return (
    <ThemeProvider>
      {(() => {
  switch (currentScreen) {
          case 'settings':
            return (
              <SettingsScreen
                onBack={() => setCurrentScreen('dashboard')}
                onLogout={handleLogout}
              />
            );
    case 'goal':
      return (
        <GoalScreen
          userName={userData.userName || 'Usuario'}
          onGoalSet={handleGoalSet}
        />
      );
    case 'dashboard':
      return (
        <Dashboard
          userName={userData.userName || 'Usuario'}
          userGoal={userData.goal}
                onSettingsClick={() => setCurrentScreen('settings')}
        />
      );
    case 'login':
    default:
      return <LoginScreen onLoginSuccess={handleLoginSuccess} />;
  }
      })()}
    </ThemeProvider>
  );
}

export default App;

