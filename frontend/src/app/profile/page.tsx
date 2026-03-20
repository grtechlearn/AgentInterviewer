'use client';

import { useState } from 'react';

const USER = {
  name: 'Priya Sharma',
  email: 'priya.sharma@example.com',
  avatar: 'PS',
  level: 12,
  xp: 4820,
  nextLevelXp: 5000,
  streak: 21,
  title: 'Interview Pro',
  totalInterviews: 47,
  avgScore: 76,
};

const ACHIEVEMENTS = [
  { icon: '🔥', name: 'Week Warrior', desc: '7-day streak', unlocked: true },
  { icon: '🎯', name: 'Sharpshooter', desc: 'Score 90%+', unlocked: true },
  { icon: '🐍', name: 'Python Master', desc: '20 Python interviews', unlocked: true },
  { icon: '⚡', name: 'Speed Demon', desc: 'Complete in <5 min', unlocked: true },
  { icon: '🏆', name: 'Top 10', desc: 'Leaderboard top 10', unlocked: false },
  { icon: '🌟', name: 'All-Rounder', desc: 'Try all domains', unlocked: false },
];

const HISTORY = [
  { domain: 'Python', score: 88, date: '2024-03-18' },
  { domain: 'React', score: 72, date: '2024-03-17' },
  { domain: 'System Design', score: 65, date: '2024-03-16' },
  { domain: 'Java', score: 91, date: '2024-03-15' },
];

export default function ProfilePage() {
  const [notifications, setNotifications] = useState(true);
  const [darkMode, setDarkMode] = useState(false);
  const [language, setLanguage] = useState('English');
  const xpProgress = Math.round((USER.xp / USER.nextLevelXp) * 100);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Profile Header */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 mb-6 flex flex-col sm:flex-row items-center gap-6">
        <div className="w-20 h-20 bg-blue-500 rounded-full flex items-center justify-center text-white text-2xl font-bold">
          {USER.avatar}
        </div>
        <div className="text-center sm:text-left flex-1">
          <h1 className="text-2xl font-bold text-gray-900">{USER.name}</h1>
          <p className="text-gray-500 text-sm">{USER.email}</p>
          <p className="text-blue-500 text-sm font-medium mt-1">{USER.title}</p>
        </div>
        <div className="flex gap-6 text-center">
          <div><p className="text-2xl font-bold text-gray-900">{USER.level}</p><p className="text-xs text-gray-400">Level</p></div>
          <div><p className="text-2xl font-bold text-blue-500">{USER.xp.toLocaleString()}</p><p className="text-xs text-gray-400">XP</p></div>
          <div><p className="text-2xl font-bold text-orange-500">{USER.streak}</p><p className="text-xs text-gray-400">Streak</p></div>
        </div>
      </div>

      {/* XP Progress */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 mb-6">
        <div className="flex justify-between text-sm mb-2">
          <span className="text-gray-600 font-medium">Level {USER.level} Progress</span>
          <span className="text-gray-400">{USER.xp} / {USER.nextLevelXp} XP</span>
        </div>
        <div className="w-full h-3 bg-gray-100 rounded-full overflow-hidden">
          <div className="h-full bg-blue-500 rounded-full" style={{ width: `${xpProgress}%` }} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Achievements */}
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Achievements</h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {ACHIEVEMENTS.map((a) => (
              <div
                key={a.name}
                className={`p-3 rounded-xl border text-center ${
                  a.unlocked ? 'border-blue-100 bg-blue-50' : 'border-gray-100 bg-gray-50 opacity-50'
                }`}
              >
                <span className="text-2xl">{a.icon}</span>
                <p className="text-xs font-semibold text-gray-900 mt-1">{a.name}</p>
                <p className="text-xs text-gray-400">{a.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Interview History */}
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Interview History</h2>
          <div className="space-y-3">
            {HISTORY.map((h, i) => (
              <div key={i} className="flex items-center justify-between py-2 border-b border-gray-50 last:border-0">
                <div>
                  <p className="text-sm font-medium text-gray-900">{h.domain}</p>
                  <p className="text-xs text-gray-400">{h.date}</p>
                </div>
                <span className={`font-semibold text-sm ${h.score >= 80 ? 'text-green-500' : h.score >= 60 ? 'text-yellow-500' : 'text-red-500'}`}>
                  {h.score}%
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Settings */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Settings</h2>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div><p className="text-sm font-medium text-gray-900">Notifications</p><p className="text-xs text-gray-400">Daily reminders and streak alerts</p></div>
            <button onClick={() => setNotifications(!notifications)} className={`w-11 h-6 rounded-full transition-colors ${notifications ? 'bg-blue-500' : 'bg-gray-300'}`}>
              <div className={`w-5 h-5 bg-white rounded-full shadow transition-transform ${notifications ? 'translate-x-5' : 'translate-x-0.5'}`} />
            </button>
          </div>
          <div className="flex items-center justify-between">
            <div><p className="text-sm font-medium text-gray-900">Dark Mode</p><p className="text-xs text-gray-400">Switch to dark theme</p></div>
            <button onClick={() => setDarkMode(!darkMode)} className={`w-11 h-6 rounded-full transition-colors ${darkMode ? 'bg-blue-500' : 'bg-gray-300'}`}>
              <div className={`w-5 h-5 bg-white rounded-full shadow transition-transform ${darkMode ? 'translate-x-5' : 'translate-x-0.5'}`} />
            </button>
          </div>
          <div className="flex items-center justify-between">
            <div><p className="text-sm font-medium text-gray-900">Language</p><p className="text-xs text-gray-400">Interface language</p></div>
            <select value={language} onChange={(e) => setLanguage(e.target.value)} className="text-sm border border-gray-200 rounded-lg px-3 py-1.5">
              <option>English</option><option>Hindi</option><option>Tamil</option><option>Telugu</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );
}
