'use client';

import { useState } from 'react';

const GOALS = [
  { id: '1', title: 'Weekly Interviews', current: 3, target: 5, unit: 'interviews' },
  { id: '2', title: 'Average Score', current: 72, target: 85, unit: '%' },
  { id: '3', title: 'Questions Practiced', current: 28, target: 50, unit: 'questions' },
  { id: '4', title: 'New Domains Explored', current: 2, target: 3, unit: 'domains' },
];

const STREAKS = [
  { week: 'W1', days: 5 }, { week: 'W2', days: 7 }, { week: 'W3', days: 4 },
  { week: 'W4', days: 6 }, { week: 'W5', days: 7 }, { week: 'W6', days: 3 },
  { week: 'W7', days: 5 }, { week: 'W8', days: 6 },
];

const MILESTONES = [
  { label: '50 Interviews', progress: 72, icon: '🎯' },
  { label: 'Score 90% in Python', progress: 85, icon: '🐍' },
  { label: '30-Day Streak', progress: 53, icon: '🔥' },
  { label: 'Master System Design', progress: 40, icon: '🏗️' },
];

export default function GoalsPage() {
  const [weeklyTarget, setWeeklyTarget] = useState(5);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Goals</h1>
        <p className="text-gray-500 mt-1">Set targets and track your weekly progress.</p>
      </div>

      {/* Weekly Target Setting */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Weekly Target</h2>
        <div className="flex items-center gap-4">
          <label className="text-sm text-gray-600">Interviews per week:</label>
          <input
            type="range" min={1} max={10} value={weeklyTarget}
            onChange={(e) => setWeeklyTarget(Number(e.target.value))}
            className="flex-1 accent-blue-500"
          />
          <span className="text-2xl font-bold text-blue-500 w-10 text-center">{weeklyTarget}</span>
        </div>
      </div>

      {/* Progress Bars */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        {GOALS.map((goal) => {
          const pct = Math.min(100, Math.round((goal.current / goal.target) * 100));
          return (
            <div key={goal.id} className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-900">{goal.title}</span>
                <span className="text-sm text-gray-500">{goal.current}/{goal.target} {goal.unit}</span>
              </div>
              <div className="w-full h-3 bg-gray-100 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full ${pct >= 100 ? 'bg-green-500' : 'bg-blue-500'}`}
                  style={{ width: `${pct}%` }}
                />
              </div>
              <p className="text-xs text-gray-400 mt-1">{pct}% complete</p>
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Streak History */}
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Streak History</h2>
          <div className="flex items-end gap-3 h-40">
            {STREAKS.map((s) => (
              <div key={s.week} className="flex-1 flex flex-col items-center gap-1">
                <div
                  className="w-full bg-blue-500 rounded-t-md"
                  style={{ height: `${(s.days / 7) * 100}%` }}
                />
                <span className="text-xs text-gray-400">{s.week}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Next Milestones */}
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Next Milestones</h2>
          <div className="space-y-4">
            {MILESTONES.map((m) => (
              <div key={m.label}>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium text-gray-900">{m.icon} {m.label}</span>
                  <span className="text-sm font-semibold text-blue-500">{m.progress}%</span>
                </div>
                <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div className="h-full bg-blue-500 rounded-full" style={{ width: `${m.progress}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
