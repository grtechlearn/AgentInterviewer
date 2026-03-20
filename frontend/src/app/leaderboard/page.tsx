'use client';

import { useState } from 'react';

const DOMAINS = ['All', 'Python', 'React', 'Java', 'System Design', 'DevOps', 'iOS', 'Android'];

const USERS = [
  { rank: 1, name: 'Priya Sharma', xp: 4820, level: 12, streak: 21, domain: 'Python' },
  { rank: 2, name: 'Arjun Patel', xp: 4350, level: 11, streak: 18, domain: 'React' },
  { rank: 3, name: 'Sneha Reddy', xp: 3980, level: 10, streak: 14, domain: 'System Design' },
  { rank: 4, name: 'Vikram Singh', xp: 3720, level: 10, streak: 12, domain: 'Java' },
  { rank: 5, name: 'Ananya Gupta', xp: 3400, level: 9, streak: 10, domain: 'Python' },
  { rank: 6, name: 'Rahul Mehta', xp: 3150, level: 9, streak: 9, domain: 'DevOps' },
  { rank: 7, name: 'Kavya Nair', xp: 2900, level: 8, streak: 7, domain: 'iOS' },
  { rank: 8, name: 'Aditya Kumar', xp: 2650, level: 8, streak: 6, domain: 'React' },
  { rank: 9, name: 'Meera Iyer', xp: 2400, level: 7, streak: 5, domain: 'Android' },
  { rank: 10, name: 'Rohan Das', xp: 2100, level: 7, streak: 4, domain: 'Java' },
];

function medalColor(rank: number) {
  if (rank === 1) return 'text-yellow-500';
  if (rank === 2) return 'text-gray-400';
  if (rank === 3) return 'text-amber-600';
  return 'text-gray-300';
}

export default function LeaderboardPage() {
  const [filter, setFilter] = useState('All');
  const filtered = filter === 'All' ? USERS : USERS.filter((u) => u.domain === filter);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Leaderboard</h1>
        <p className="text-gray-500 mt-1">Weekly rankings across all domains.</p>
      </div>

      {/* Domain Filter */}
      <div className="flex flex-wrap gap-2 mb-6">
        {DOMAINS.map((d) => (
          <button
            key={d}
            onClick={() => setFilter(d)}
            className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
              filter === d ? 'bg-blue-500 text-white' : 'bg-white text-gray-600 border border-gray-200 hover:bg-blue-50'
            }`}
          >
            {d}
          </button>
        ))}
      </div>

      {/* Rankings Table */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-gray-400 border-b border-gray-100 bg-slate-50">
                <th className="px-6 py-4 font-medium">Rank</th>
                <th className="px-6 py-4 font-medium">Name</th>
                <th className="px-6 py-4 font-medium">XP</th>
                <th className="px-6 py-4 font-medium">Level</th>
                <th className="px-6 py-4 font-medium">Streak</th>
                <th className="px-6 py-4 font-medium">Domain</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((user) => (
                <tr key={user.rank} className="border-b border-gray-50 last:border-0 hover:bg-slate-50">
                  <td className={`px-6 py-4 font-bold text-lg ${medalColor(user.rank)}`}>
                    {user.rank <= 3 ? ['', '🥇', '🥈', '🥉'][user.rank] : `#${user.rank}`}
                  </td>
                  <td className="px-6 py-4 font-medium text-gray-900">{user.name}</td>
                  <td className="px-6 py-4 font-semibold text-blue-500">{user.xp.toLocaleString()}</td>
                  <td className="px-6 py-4 text-gray-600">Lv.{user.level}</td>
                  <td className="px-6 py-4 text-gray-600">{user.streak} days</td>
                  <td className="px-6 py-4">
                    <span className="px-2.5 py-1 text-xs font-medium bg-blue-50 text-blue-600 rounded-full">
                      {user.domain}
                    </span>
                  </td>
                </tr>
              ))}
              {filtered.length === 0 && (
                <tr><td colSpan={6} className="px-6 py-8 text-center text-gray-400">No users found.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
