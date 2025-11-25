import React, { useState, useEffect } from 'react';
import { Flame, Send, Coffee, ShoppingBag, Utensils, Settings } from 'lucide-react';
import api from '../services/api';

// Discord Logo SVG Component
const DiscordIcon = () => (
  <svg width="16" height="16" viewBox="0 0 71 55" fill="currentColor">
    <path d="M60.1045 4.8978C55.5792 2.8214 50.7265 1.2916 45.6527 0.41542C45.5603 0.39851 45.468 0.440769 45.4204 0.525289C44.7963 1.6353 44.105 3.0834 43.6209 4.2216C38.1637 3.4046 32.7345 3.4046 27.3892 4.2216C26.905 3.0581 26.1886 1.6353 25.5617 0.525289C25.5141 0.443589 25.4218 0.40133 25.3294 0.41542C20.2584 1.2888 15.4057 2.8186 10.8776 4.8978C10.8384 4.9147 10.8048 4.9429 10.7825 4.9795C1.57795 18.7309 -0.943561 32.1443 0.293408 45.3914C0.299005 45.4562 0.335386 45.5182 0.385761 45.5576C6.45866 50.0174 12.3413 52.7249 18.1147 54.5195C18.2071 54.5477 18.305 54.5139 18.3638 54.4378C19.7295 52.5728 20.9469 50.6063 21.9907 48.5383C22.0523 48.4172 21.9935 48.2735 21.8676 48.2256C19.9366 47.4931 18.0979 46.6 16.3292 45.5858C16.1893 45.5041 16.1781 45.304 16.3068 45.2082C16.679 44.9293 17.0513 44.6391 17.4067 44.3461C17.471 44.2926 17.5606 44.2813 17.6362 44.3151C29.2558 49.6202 41.8354 49.6202 53.3179 44.3151C53.3935 44.2785 53.4831 44.2898 53.5502 44.3433C53.9057 44.6363 54.2779 44.9293 54.6529 45.2082C54.7816 45.304 54.7732 45.5041 54.6333 45.5858C52.8646 46.6197 51.0259 47.4931 49.0921 48.2228C48.9662 48.2707 48.9102 48.4172 48.9718 48.5383C50.038 50.6034 51.2554 52.5699 52.5959 54.435C52.6519 54.5139 52.7526 54.5477 52.845 54.5195C58.6464 52.7249 64.529 50.0174 70.6019 45.5576C70.6551 45.5182 70.6887 45.459 70.6943 45.3942C72.1747 30.0791 68.2147 16.7757 60.1968 4.9823C60.1772 4.9429 60.1437 4.9147 60.1045 4.8978ZM23.7259 37.3253C20.2276 37.3253 17.3451 34.1136 17.3451 30.1693C17.3451 26.225 20.1717 23.0133 23.7259 23.0133C27.308 23.0133 30.1626 26.2532 30.1066 30.1693C30.1066 34.1136 27.28 37.3253 23.7259 37.3253ZM47.3178 37.3253C43.8196 37.3253 40.9371 34.1136 40.9371 30.1693C40.9371 26.225 43.7636 23.0133 47.3178 23.0133C50.9 23.0133 53.7545 26.2532 53.6986 30.1693C53.6986 34.1136 50.9 37.3253 47.3178 37.3253Z"/>
  </svg>
);

const getCategoryIcon = (category) => {
  if (!category) return Utensils;
  const catLower = category.toLowerCase();
  if (catLower.includes('comida') || catLower.includes('food')) return Utensils;
  if (catLower.includes('café') || catLower.includes('coffee')) return Coffee;
  if (catLower.includes('compras') || catLower.includes('shopping')) return ShoppingBag;
  return Utensils;
};

const getCategoryName = (category) => {
  if (!category) return 'Otros';
  const catLower = category.toLowerCase();
  if (catLower.includes('comida') || catLower.includes('food')) return 'Comida';
  if (catLower.includes('café') || catLower.includes('coffee')) return 'Café';
  if (catLower.includes('compras') || catLower.includes('shopping')) return 'Compras';
  return category.replace(/[🍔🚗🎮🏠👗💊📚✈️🎁📱💡💰💼❓]/g, '').trim() || 'Otros';
};

export default function Dashboard({ userName, userGoal, onSettingsClick }) {
  const [expense, setExpense] = useState('');
  const [streak, setStreak] = useState(0);
  const [recentExpenses, setRecentExpenses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [streakLoading, setStreakLoading] = useState(true);

  const googleId = localStorage.getItem('google_id');

  // Cargar datos al montar
  useEffect(() => {
    if (googleId) {
      loadStreak();
      loadRecentExpenses();
    }
  }, [googleId]);

  const loadStreak = async () => {
    if (!googleId) return;
    try {
      setStreakLoading(true);
      const data = await api.getRacha(googleId);
      setStreak(data.current_streak || 0);
    } catch (error) {
      console.error('Error cargando racha:', error);
    } finally {
      setStreakLoading(false);
    }
  };

  const loadRecentExpenses = async () => {
    if (!googleId) return;
    try {
      const data = await api.getGastos(googleId, 20);
      setRecentExpenses(data.gastos || []);
    } catch (error) {
      console.error('Error cargando gastos:', error);
    }
  };

  const handleSendExpense = async () => {
    if (!expense.trim() || loading || !googleId) return;

    setLoading(true);
    try {
      await api.crearGasto(expense.trim(), googleId);
      setExpense('');
      // Recargar datos
      await Promise.all([loadStreak(), loadRecentExpenses()]);
    } catch (error) {
      console.error('Error enviando gasto:', error);
      alert('Error al registrar el gasto. Por favor, intenta de nuevo.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !loading) {
      handleSendExpense();
    }
  };

  return (
    <div className="min-h-screen bg-white dark:bg-slate-950 text-slate-950 dark:text-white flex flex-col">
      {/* Header */}
      <header className="px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-semibold">
          Hola, {userName} 👋
        </h1>
        <div className="flex items-center gap-3">
          <button
            onClick={() => onSettingsClick && onSettingsClick()}
            className="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full transition-colors"
          >
            <Settings size={20} className="text-slate-600 dark:text-slate-400" />
          </button>
        <a 
          href="https://discord.gg/C8t2qmDa2S"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 bg-gradient-to-r from-indigo-500 to-indigo-600 text-white px-3 py-1.5 rounded-full text-sm font-semibold hover:from-indigo-400 hover:to-indigo-500 transition-all"
        >
          <DiscordIcon />
          Discord VIP
        </a>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 px-6 pb-24 overflow-y-auto">
        {/* Hero Section - Streak Ring */}
        <div className="flex flex-col items-center justify-center py-8 mt-4">
          <div className="relative">
            {/* Animated Ring */}
            <div className="relative w-52 h-52">
              {/* Outer Glow */}
              <div className="absolute inset-0 rounded-full bg-gradient-to-r from-orange-500 to-red-500 opacity-20 blur-xl animate-pulse"></div>
              
              {/* Main Ring */}
              <svg className="w-full h-full transform -rotate-90" viewBox="0 0 200 200">
                {/* Background Circle */}
                <circle
                  cx="100"
                  cy="100"
                  r="85"
                  fill="none"
                  stroke="rgba(148, 163, 184, 0.1)"
                  strokeWidth="12"
                />
                {/* Progress Circle */}
                <circle
                  cx="100"
                  cy="100"
                  r="85"
                  fill="none"
                  stroke="url(#gradient)"
                  strokeWidth="12"
                  strokeLinecap="round"
                  strokeDasharray={`${(streak / 7) * 534} 534`}
                  className="transition-all duration-1000"
                />
                <defs>
                  <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#f97316" />
                    <stop offset="100%" stopColor="#ef4444" />
                  </linearGradient>
                </defs>
              </svg>
              
              {/* Center Content */}
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <Flame className="text-orange-500 mb-2 animate-pulse" size={48} />
                <div className="text-5xl font-bold bg-gradient-to-r from-orange-400 to-red-500 bg-clip-text text-transparent">
                  {streakLoading ? '...' : streak}
                </div>
                <div className="text-slate-400 text-sm mt-1">Días</div>
              </div>
            </div>
          </div>
          
          {/* Status Text */}
          <p className="mt-6 text-emerald-600 dark:text-emerald-400 text-sm font-medium">
            ✓ Tu racha está a salvo
          </p>
        </div>

        {/* Recent Activity Feed */}
        <div className="mt-8">
          <h2 className="text-lg font-semibold mb-4 text-slate-700 dark:text-slate-300">Patrones de Gasto Recientes</h2>
          {recentExpenses.length === 0 ? (
            <div className="text-center py-8 text-slate-500 dark:text-slate-400">
              <p>No hay gastos registrados aún.</p>
              <p className="text-sm mt-2">¡Registra tu primer gasto abajo!</p>
            </div>
          ) : (
            <div className="space-y-3">
              {recentExpenses.map((item) => {
                const Icon = getCategoryIcon(item.category);
                return (
                  <div 
                    key={item.id}
                    className="bg-slate-100 dark:bg-slate-900 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 transition-colors"
                  >
                    <div className="flex items-start gap-3">
                      <div className="bg-slate-200 dark:bg-slate-800 p-2.5 rounded-xl">
                        <Icon size={20} className="text-slate-600 dark:text-slate-400" />
                      </div>
                      <div className="flex-1">
                        <div className="flex justify-between items-center mb-1">
                          <span className="text-slate-700 dark:text-slate-300 font-medium">
                            {getCategoryName(item.category)}
                          </span>
                          <span className="text-red-500 dark:text-red-400 font-semibold">
                            {item.amount ? `-${item.amount}€` : '-'}
                          </span>
                        </div>
                        {item.raw_text && (
                          <p className="text-slate-600 dark:text-slate-500 text-xs mb-1">
                            {item.raw_text}
                          </p>
                        )}
                        {item.aury_response && (
                          <p className="text-slate-600 dark:text-slate-500 text-sm italic">
                            {item.aury_response}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </main>

      {/* Sticky Bottom Input */}
      <div className="fixed bottom-0 left-0 right-0 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 px-6 py-4">
        <div className="flex items-center gap-3 max-w-2xl mx-auto">
          <input
            type="text"
            value={expense}
            onChange={(e) => setExpense(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Escribe tu gasto... (ej: Cena 20€)"
            className="flex-1 bg-slate-100 dark:bg-slate-800 text-slate-950 dark:text-white placeholder-slate-500 dark:placeholder-slate-400 rounded-full px-5 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all"
            disabled={loading}
          />
          <button
            onClick={handleSendExpense}
            className="bg-gradient-to-r from-emerald-500 to-emerald-600 p-3 rounded-full hover:from-emerald-400 hover:to-emerald-500 transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={!expense.trim() || loading}
          >
            <Send size={20} className="text-white" />
          </button>
        </div>
      </div>
    </div>
  );
}

