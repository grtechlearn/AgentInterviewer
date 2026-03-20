'use client';

import { useState } from 'react';

const MY_GROUPS = [
  {
    id: '1', name: 'Python Warriors', members: 12, task: 'Complete 5 Python interviews this week',
    leaderboard: [
      { name: 'Priya S.', score: 92 }, { name: 'Arjun P.', score: 87 }, { name: 'Sneha R.', score: 81 },
    ],
  },
  {
    id: '2', name: 'FAANG Prep Club', members: 24, task: 'System design mock every Sunday',
    leaderboard: [
      { name: 'Vikram S.', score: 88 }, { name: 'Kavya N.', score: 85 }, { name: 'Rahul M.', score: 79 },
    ],
  },
  {
    id: '3', name: 'React Study Group', members: 8, task: 'Build a portfolio project together',
    leaderboard: [
      { name: 'Aditya K.', score: 90 }, { name: 'Meera I.', score: 84 }, { name: 'Rohan D.', score: 77 },
    ],
  },
];

const DISCOVER = [
  { name: 'Java Enthusiasts', members: 32, domain: 'Java' },
  { name: 'DevOps Daily', members: 18, domain: 'DevOps' },
  { name: 'iOS Learners', members: 14, domain: 'iOS' },
  { name: 'Campus Placement Prep', members: 56, domain: 'General' },
];

export default function GroupsPage() {
  const [showCreate, setShowCreate] = useState(false);
  const [expanded, setExpanded] = useState<string | null>(null);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Groups</h1>
          <p className="text-gray-500 mt-1">Practice together and stay accountable.</p>
        </div>
        <button
          onClick={() => setShowCreate(!showCreate)}
          className="px-5 py-2.5 bg-blue-500 text-white text-sm font-semibold rounded-lg hover:bg-blue-600 transition-colors"
        >
          Create Group
        </button>
      </div>

      {/* Create Group Form */}
      {showCreate && (
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">New Group</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <input placeholder="Group name" className="px-4 py-2.5 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            <select className="px-4 py-2.5 border border-gray-200 rounded-lg text-sm">
              <option>Python</option><option>React</option><option>Java</option><option>System Design</option><option>General</option>
            </select>
          </div>
          <textarea placeholder="Group description and weekly task..." rows={2} className="w-full mt-3 px-4 py-2.5 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <button className="mt-3 px-5 py-2 bg-blue-500 text-white text-sm font-semibold rounded-lg hover:bg-blue-600">Create</button>
        </div>
      )}

      {/* My Groups */}
      <h2 className="text-xl font-bold text-gray-900 mb-4">My Groups</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        {MY_GROUPS.map((group) => (
          <div key={group.id} className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900">{group.name}</h3>
            <p className="text-sm text-gray-400 mt-1">{group.members} members</p>
            <div className="mt-3 p-3 bg-blue-50 rounded-lg">
              <p className="text-xs text-blue-600 font-medium">Weekly Task</p>
              <p className="text-sm text-gray-700 mt-0.5">{group.task}</p>
            </div>
            <button
              onClick={() => setExpanded(expanded === group.id ? null : group.id)}
              className="text-sm text-blue-500 font-medium mt-3 hover:underline"
            >
              {expanded === group.id ? 'Hide' : 'Show'} Leaderboard
            </button>
            {expanded === group.id && (
              <div className="mt-3 space-y-2">
                {group.leaderboard.map((m, i) => (
                  <div key={m.name} className="flex items-center justify-between text-sm">
                    <span className="text-gray-700">{i + 1}. {m.name}</span>
                    <span className="font-semibold text-blue-500">{m.score}%</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Discover Groups */}
      <h2 className="text-xl font-bold text-gray-900 mb-4">Discover Groups</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {DISCOVER.map((g) => (
          <div key={g.name} className="bg-white rounded-xl border border-gray-100 shadow-sm p-5 flex flex-col">
            <h3 className="font-semibold text-gray-900">{g.name}</h3>
            <p className="text-xs text-gray-400 mt-1">{g.members} members</p>
            <span className="mt-2 px-2 py-1 text-xs font-medium bg-blue-50 text-blue-600 rounded-full w-fit">{g.domain}</span>
            <button className="mt-auto pt-3 text-sm text-blue-500 font-medium hover:underline">Join Group</button>
          </div>
        ))}
      </div>
    </div>
  );
}
