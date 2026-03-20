const STATS = [
  { label: 'Total Users', value: '2,847', change: '+12%', color: 'text-blue-500' },
  { label: 'Interviews Today', value: '384', change: '+8%', color: 'text-green-500' },
  { label: 'API Cost (MTD)', value: '$142.30', change: '-3%', color: 'text-purple-500' },
  { label: 'Avg Response Time', value: '1.2s', change: '-15%', color: 'text-orange-500' },
];

const AGENTS = [
  { name: 'Python Interviewer', status: 'active', interviews: 1240, avgScore: 74 },
  { name: 'React Interviewer', status: 'active', interviews: 980, avgScore: 71 },
  { name: 'System Design Agent', status: 'active', interviews: 620, avgScore: 65 },
  { name: 'Java Interviewer', status: 'maintenance', interviews: 850, avgScore: 78 },
  { name: 'DevOps Agent', status: 'active', interviews: 410, avgScore: 62 },
  { name: 'HR Interviewer', status: 'inactive', interviews: 190, avgScore: 80 },
];

const ACTIVITY = [
  { time: '2 min ago', event: 'New user registered: meera.iyer@gmail.com', type: 'user' },
  { time: '5 min ago', event: 'Python interview completed (score: 88%)', type: 'interview' },
  { time: '12 min ago', event: 'API rate limit warning: 85% capacity', type: 'warning' },
  { time: '18 min ago', event: 'React agent restarted successfully', type: 'system' },
  { time: '25 min ago', event: 'New subscription: Pro plan (INR 999)', type: 'billing' },
  { time: '1 hr ago', event: 'Daily backup completed', type: 'system' },
];

function statusBadge(status: string) {
  const styles: Record<string, string> = {
    active: 'bg-green-50 text-green-600',
    maintenance: 'bg-yellow-50 text-yellow-600',
    inactive: 'bg-gray-100 text-gray-500',
  };
  return styles[status] || styles.inactive;
}

export default function AdminPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
        <p className="text-gray-500 mt-1">System overview and management.</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {STATS.map((s) => (
          <div key={s.label} className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
            <p className="text-sm text-gray-500 font-medium">{s.label}</p>
            <p className={`text-3xl font-bold mt-1 ${s.color}`}>{s.value}</p>
            <p className="text-xs text-gray-400 mt-1">{s.change} vs last week</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Agent List */}
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Agents</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-gray-400 border-b border-gray-50">
                  <th className="pb-3 font-medium">Agent</th>
                  <th className="pb-3 font-medium">Status</th>
                  <th className="pb-3 font-medium">Interviews</th>
                  <th className="pb-3 font-medium">Avg Score</th>
                </tr>
              </thead>
              <tbody>
                {AGENTS.map((a) => (
                  <tr key={a.name} className="border-b border-gray-50 last:border-0">
                    <td className="py-3 font-medium text-gray-900">{a.name}</td>
                    <td className="py-3">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${statusBadge(a.status)}`}>
                        {a.status}
                      </span>
                    </td>
                    <td className="py-3 text-gray-500">{a.interviews.toLocaleString()}</td>
                    <td className="py-3 text-gray-500">{a.avgScore}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Activity Feed */}
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h2>
          <div className="space-y-4">
            {ACTIVITY.map((a, i) => (
              <div key={i} className="flex gap-3">
                <div className="w-2 h-2 mt-2 rounded-full bg-blue-500 shrink-0" />
                <div>
                  <p className="text-sm text-gray-700">{a.event}</p>
                  <p className="text-xs text-gray-400 mt-0.5">{a.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
