import Link from 'next/link';

const TIERS = [
  {
    name: 'Free',
    price: '0',
    period: '',
    description: 'Get started with basic practice',
    features: ['3 interviews / week', '2 domains', 'Basic feedback', 'Community forums'],
    cta: 'Start Free',
    highlight: false,
  },
  {
    name: 'Starter',
    price: '499',
    period: '/mo',
    description: 'For serious job seekers',
    features: ['10 interviews / week', '5 domains', 'Detailed feedback', 'Score analytics', 'Quiz mode'],
    cta: 'Get Starter',
    highlight: false,
  },
  {
    name: 'Pro',
    price: '999',
    period: '/mo',
    description: 'Unlock everything',
    features: [
      'Unlimited interviews', 'All domains', 'AI study plans', 'Priority support',
      'Mock HR rounds', 'Group practice', 'Leaderboard access',
    ],
    cta: 'Get Pro',
    highlight: true,
  },
  {
    name: 'Enterprise',
    price: 'Custom',
    period: '',
    description: 'For teams and colleges',
    features: [
      'Everything in Pro', 'Custom domains', 'Admin dashboard', 'Bulk onboarding',
      'API access', 'Dedicated support', 'Analytics exports',
    ],
    cta: 'Contact Sales',
    highlight: false,
  },
];

const COMPARISON = [
  { feature: 'Interviews / week', free: '3', starter: '10', pro: 'Unlimited', enterprise: 'Unlimited' },
  { feature: 'Domains', free: '2', starter: '5', pro: 'All', enterprise: 'Custom' },
  { feature: 'Feedback depth', free: 'Basic', starter: 'Detailed', pro: 'AI-powered', enterprise: 'AI-powered' },
  { feature: 'Quiz mode', free: '--', starter: 'Yes', pro: 'Yes', enterprise: 'Yes' },
  { feature: 'Study plans', free: '--', starter: '--', pro: 'Yes', enterprise: 'Yes' },
  { feature: 'Admin dashboard', free: '--', starter: '--', pro: '--', enterprise: 'Yes' },
];

export default function PricingPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-extrabold text-gray-900">Simple, Transparent Pricing</h1>
        <p className="text-gray-500 mt-3 text-lg">Start free. Upgrade when you need more.</p>
      </div>

      {/* Tier Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
        {TIERS.map((tier) => (
          <div
            key={tier.name}
            className={`rounded-xl border p-6 flex flex-col ${
              tier.highlight
                ? 'border-blue-500 shadow-lg shadow-blue-500/10 ring-2 ring-blue-500'
                : 'border-gray-100 shadow-sm'
            }`}
          >
            {tier.highlight && (
              <span className="text-xs font-bold text-blue-500 uppercase tracking-wide mb-2">Most Popular</span>
            )}
            <h3 className="text-xl font-bold text-gray-900">{tier.name}</h3>
            <p className="text-sm text-gray-500 mt-1">{tier.description}</p>
            <div className="mt-4 mb-6">
              {tier.price === 'Custom' ? (
                <span className="text-3xl font-extrabold text-gray-900">Contact Us</span>
              ) : (
                <>
                  <span className="text-sm text-gray-500">INR </span>
                  <span className="text-4xl font-extrabold text-gray-900">{tier.price}</span>
                  <span className="text-sm text-gray-500">{tier.period}</span>
                </>
              )}
            </div>
            <ul className="space-y-2 mb-6 flex-1">
              {tier.features.map((f) => (
                <li key={f} className="flex items-center gap-2 text-sm text-gray-600">
                  <span className="text-blue-500">&#10003;</span> {f}
                </li>
              ))}
            </ul>
            <Link
              href="/login"
              className={`block text-center py-2.5 rounded-lg font-semibold text-sm transition-colors ${
                tier.highlight
                  ? 'bg-blue-500 text-white hover:bg-blue-600'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {tier.cta}
            </Link>
          </div>
        ))}
      </div>

      {/* Feature Comparison */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        <h2 className="text-lg font-semibold text-gray-900 p-6 pb-0">Feature Comparison</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm mt-4">
            <thead>
              <tr className="text-left text-gray-400 border-b border-gray-100">
                <th className="px-6 py-3 font-medium">Feature</th>
                <th className="px-6 py-3 font-medium">Free</th>
                <th className="px-6 py-3 font-medium">Starter</th>
                <th className="px-6 py-3 font-medium text-blue-500">Pro</th>
                <th className="px-6 py-3 font-medium">Enterprise</th>
              </tr>
            </thead>
            <tbody>
              {COMPARISON.map((row) => (
                <tr key={row.feature} className="border-b border-gray-50 last:border-0">
                  <td className="px-6 py-3 font-medium text-gray-900">{row.feature}</td>
                  <td className="px-6 py-3 text-gray-500">{row.free}</td>
                  <td className="px-6 py-3 text-gray-500">{row.starter}</td>
                  <td className="px-6 py-3 text-blue-600 font-medium">{row.pro}</td>
                  <td className="px-6 py-3 text-gray-500">{row.enterprise}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
