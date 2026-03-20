'use client';

import { useUser } from '@/hooks/useUser';
import SkillMap from '@/components/SkillMap';
import XPBar from '@/components/XPBar';
import StreakCounter from '@/components/StreakCounter';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const SCORE_TREND = [
  { date: 'Mon', score: 62 },
  { date: 'Tue', score: 68 },
  { date: 'Wed', score: 71 },
  { date: 'Thu', score: 65 },
  { date: 'Fri', score: 78 },
  { date: 'Sat', score: 82 },
  { date: 'Sun', score: 85 },
];

const RECENT_INTERVIEWS = [
  { id: 1, domain: 'Python', score: 85, date: '2024-03-18', questions: 10 },
  { id: 2, domain: 'React', score: 72, date: '2024-03-17', questions: 5 },
  { id: 3, domain: 'System Design', score: 68, date: '2024-03-16', questions: 5 },
  { id: 4, domain: 'Java', score: 90, date: '2024-03-15', questions: 10 },
  { id: 5, domain: 'DevOps', score: 55, date: '2024-03-14', questions: 5 },
];

const WEAK_AREAS = [
  { domain: 'iOS', topic: 'SwiftUI Layouts', score: 35 },
  { domain: 'DevOps', topic: 'Kubernetes Networking', score: 42 },
  { domain: 'System Design', topic: 'Database Sharding', score: 48 },
  { domain: 'Android', topic: 'Jetpack Compose', score: 50 },
];

export default function DashboardPage() {
  const { user, xpForNextLevel, xpProgress } = useUser();

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-500 mt-1">Track your interview preparation progress.</p>
      </div>

      {/* Top Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
          <StreakCounter streak={user.streak} />
        </div>
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
          <XPBar xp={user.xp} level={user.level} nextLevelXp={xpForNextLevel} progress={xpProgress} />
        </div>
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
          <div className="text-sm text-gray-500 font-medium mb-1">Total Interviews</div>
          <div className="text-3xl font-bold text-gray-900">{user.totalInterviews}</div>
          <div className="text-sm text-gray-400 mt-1">Avg Score: {user.avgScore}%</div>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Skill Radar */}
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Skill Map</h2>
          <SkillMap skills={user.skills} />
        </div>

        {/* Score Trend */}
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Score Trend</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={SCORE_TREND}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="date" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#94a3b8" fontSize={12} domain={[0, 100]} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#fff',
                    border: '1px solid #e2e8f0',
                    borderRadius: '8px',
                    fontSize: '13px',
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="score"
                  stroke="#3B82F6"
                  strokeWidth={2.5}
                  dot={{ fill: '#3B82F6', r: 4 }}
                  activeDot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Interviews */}
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Interviews</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-gray-400 border-b border-gray-50">
                  <th className="pb-3 font-medium">Domain</th>
                  <th className="pb-3 font-medium">Score</th>
                  <th className="pb-3 font-medium">Questions</th>
                  <th className="pb-3 font-medium">Date</th>
                </tr>
              </thead>
              <tbody>
                {RECENT_INTERVIEWS.map((item) => (
                  <tr key={item.id} className="border-b border-gray-50 last:border-0">
                    <td className="py-3 font-medium text-gray-900">{item.domain}</td>
                    <td className="py-3">
                      <span className={`font-semibold ${
                        item.score >= 80 ? 'text-green-500' : item.score >= 60 ? 'text-yellow-500' : 'text-red-500'
                      }`}>
                        {item.score}%
                      </span>
                    </td>
                    <td className="py-3 text-gray-500">{item.questions}</td>
                    <td className="py-3 text-gray-400">{item.date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Weak Areas */}
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Areas to Improve</h2>
          <div className="space-y-4">
            {WEAK_AREAS.map((area) => (
              <div key={area.topic}>
                <div className="flex items-center justify-between mb-1.5">
                  <div>
                    <span className="text-sm font-medium text-gray-900">{area.topic}</span>
                    <span className="text-xs text-gray-400 ml-2">{area.domain}</span>
                  </div>
                  <span className="text-sm font-semibold text-red-500">{area.score}%</span>
                </div>
                <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-red-400 rounded-full"
                    style={{ width: `${area.score}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
