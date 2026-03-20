import Link from 'next/link';

const DOMAINS = [
  { name: 'Python', emoji: '🐍', color: 'bg-yellow-50 border-yellow-200' },
  { name: 'React', emoji: '⚛️', color: 'bg-cyan-50 border-cyan-200' },
  { name: 'iOS', emoji: '🍎', color: 'bg-gray-50 border-gray-200' },
  { name: 'Android', emoji: '🤖', color: 'bg-green-50 border-green-200' },
  { name: 'Java', emoji: '☕', color: 'bg-orange-50 border-orange-200' },
  { name: 'DevOps', emoji: '🔧', color: 'bg-purple-50 border-purple-200' },
  { name: 'System Design', emoji: '🏗️', color: 'bg-blue-50 border-blue-200' },
  { name: 'HR', emoji: '🤝', color: 'bg-pink-50 border-pink-200' },
];

const STATS = [
  { value: '10K+', label: 'Active Users' },
  { value: '50K+', label: 'Interviews Completed' },
  { value: '10', label: 'Tech Domains' },
];

export default function HomePage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-purple-50" />
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-24 text-center">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-gray-900 tracking-tight text-balance">
            Master Your Next Tech
            <br />
            <span className="text-blue-500">Interview with AI</span>
          </h1>
          <p className="mt-6 text-lg sm:text-xl text-gray-500 max-w-2xl mx-auto">
            Practice with an AI interviewer that adapts to your skill level.
            Get instant feedback, track your progress, and land your dream job.
          </p>
          <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/interview"
              className="inline-flex items-center justify-center px-8 py-3.5 bg-blue-500 text-white font-semibold rounded-xl hover:bg-blue-600 transition-colors shadow-lg shadow-blue-500/25 text-lg"
            >
              Start Free Interview
            </Link>
            <Link
              href="/dashboard"
              className="inline-flex items-center justify-center px-8 py-3.5 bg-white text-gray-700 font-semibold rounded-xl border border-gray-200 hover:bg-gray-50 transition-colors text-lg"
            >
              View Dashboard
            </Link>
          </div>
        </div>
      </section>

      {/* Domain Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-4">Choose Your Domain</h2>
        <p className="text-center text-gray-500 mb-12 max-w-xl mx-auto">
          Practice interviews across multiple technology domains with questions tailored to your experience level.
        </p>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
          {DOMAINS.map((domain) => (
            <Link
              key={domain.name}
              href={`/interview?domain=${domain.name.toLowerCase().replace(' ', '')}`}
              className={`group flex flex-col items-center gap-3 p-6 rounded-xl border ${domain.color} hover:shadow-md transition-all hover:-translate-y-0.5`}
            >
              <span className="text-4xl group-hover:scale-110 transition-transform">{domain.emoji}</span>
              <span className="font-semibold text-gray-700">{domain.name}</span>
            </Link>
          ))}
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-slate-50 border-y border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="grid grid-cols-3 gap-8">
            {STATS.map((stat) => (
              <div key={stat.label} className="text-center">
                <div className="text-3xl sm:text-4xl font-extrabold text-blue-500">{stat.value}</div>
                <div className="mt-2 text-sm sm:text-base text-gray-500 font-medium">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 text-center text-gray-400 text-sm">
        <p>&copy; 2024 AgentInterviewer. AI-powered interview preparation.</p>
      </footer>
    </div>
  );
}
