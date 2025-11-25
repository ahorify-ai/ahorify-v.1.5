import React, { useState } from 'react';
import api from '../services/api';

export default function GoalScreen({ userName, onGoalSet }) {
  const [goal, setGoal] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!goal.trim() || loading) return;

    const googleId = localStorage.getItem('google_id');
    if (!googleId) {
      alert('Error: No se encontró el ID de usuario');
      return;
    }

    setLoading(true);
    try {
      await api.setGoal(googleId, goal.trim());
      onGoalSet(goal.trim());
    } catch (error) {
      console.error('Error guardando objetivo:', error);
      alert('Error al guardar tu objetivo. Por favor, intenta de nuevo.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !loading) {
      handleSubmit();
    }
  };

  return (
    <div className="min-h-screen bg-white dark:bg-slate-950 text-slate-950 dark:text-white flex flex-col items-center justify-center px-6 relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-50 via-white to-slate-100 dark:from-slate-900 dark:via-slate-950 dark:to-zinc-950 opacity-50"></div>
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl animate-pulse delay-700"></div>

      {/* Content */}
      <div className="relative z-10 max-w-lg w-full">
        {/* Icon */}
        <div className="flex justify-center mb-8">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-emerald-500 to-emerald-600 opacity-20 blur-2xl rounded-full"></div>
            <div className="relative p-5">
              <img 
                src="/ahorify_icon.png" 
                alt="Ahorify Logo" 
                className="w-16 h-16 object-contain drop-shadow-2xl brightness-110"
              />
            </div>
          </div>
        </div>

        {/* Title */}
        <h1 className="text-4xl md:text-5xl font-bold mb-3 text-center">
          <span className="bg-gradient-to-r from-slate-900 to-slate-700 dark:from-white dark:to-slate-300 bg-clip-text text-transparent">
            Un momento, {userName}...
          </span>
        </h1>

        {/* Subtitle */}
        <p className="text-slate-600 dark:text-slate-400 text-lg mb-8 text-center leading-relaxed">
          Para poder ayudarte, necesito saber una cosa.
        </p>

        {/* Question */}
        <div className="bg-slate-50/80 dark:bg-slate-900/50 backdrop-blur-sm border border-slate-200 dark:border-slate-800 rounded-3xl p-8 mb-6">
          <h2 className="text-2xl font-semibold mb-6 text-center bg-gradient-to-r from-emerald-500 to-emerald-600 dark:from-emerald-400 dark:to-emerald-600 bg-clip-text text-transparent">
            ¿Para qué estás ahorrando?
          </h2>

          {/* Input */}
          <div className="relative mb-6">
            <input
              type="text"
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ej: Viaje a Japón, Coche nuevo, Jubilarme joven..."
              className="w-full bg-white dark:bg-slate-800 text-slate-950 dark:text-white placeholder-slate-500 dark:placeholder-slate-400 rounded-2xl px-6 py-4 text-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all border border-slate-300 dark:border-slate-700"
              autoFocus
              disabled={loading}
            />
          </div>

          {/* Submit Button */}
          <button
            onClick={handleSubmit}
            disabled={!goal.trim() || loading}
            className="w-full bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-400 hover:to-emerald-500 text-white font-semibold py-4 px-6 rounded-2xl flex items-center justify-center gap-2 transition-all transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 shadow-xl shadow-emerald-500/20"
          >
            {loading ? 'Guardando...' : 'Confirmar Objetivo y Empezar'}
            {!loading && <img src="/ahorify_icon.png" alt="Ahorify" className="w-5 h-5 object-contain drop-shadow-sm brightness-110" />}
          </button>
        </div>

        {/* Bottom Helper Text */}
        <p className="text-slate-500 dark:text-slate-600 text-sm text-center">
          Esto me ayudará a darte recomendaciones más certeras y mis diagnósticos más fríos y sin excusas.
        </p>
      </div>
    </div>
  );
}

