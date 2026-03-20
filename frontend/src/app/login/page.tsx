import Link from 'next/link';

const PROVIDERS = [
  { name: 'Google', icon: 'G', bg: 'bg-white border border-gray-200 hover:bg-gray-50', text: 'text-gray-700' },
  { name: 'Apple', icon: '', bg: 'bg-black hover:bg-gray-900', text: 'text-white' },
  { name: 'GitHub', icon: '', bg: 'bg-gray-800 hover:bg-gray-700', text: 'text-white' },
];

export default function LoginPage() {
  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-4 bg-slate-50">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-8">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center mx-auto mb-4">
              <span className="text-white font-bold text-lg">AI</span>
            </div>
            <h1 className="text-2xl font-bold text-gray-900">Welcome back</h1>
            <p className="text-gray-500 text-sm mt-1">Sign in to continue your interview prep</p>
          </div>

          {/* Social Login Buttons */}
          <div className="space-y-3 mb-6">
            {PROVIDERS.map((p) => (
              <button
                key={p.name}
                className={`w-full flex items-center justify-center gap-3 py-3 rounded-xl font-medium text-sm transition-colors ${p.bg} ${p.text}`}
              >
                <span className="text-lg">{p.icon}</span>
                Continue with {p.name}
              </button>
            ))}
          </div>

          {/* Divider */}
          <div className="flex items-center gap-3 mb-6">
            <div className="flex-1 h-px bg-gray-200" />
            <span className="text-xs text-gray-400 uppercase">or</span>
            <div className="flex-1 h-px bg-gray-200" />
          </div>

          {/* Email Login */}
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                type="email"
                placeholder="you@example.com"
                className="w-full px-4 py-2.5 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <button className="w-full py-2.5 bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-600 transition-colors text-sm">
              Continue with Email
            </button>
          </div>

          {/* Footer */}
          <p className="text-center text-xs text-gray-400 mt-6">
            Don&apos;t have an account?{' '}
            <Link href="/onboarding" className="text-blue-500 hover:underline font-medium">
              Sign up free
            </Link>
          </p>
        </div>

        <p className="text-center text-xs text-gray-400 mt-4">
          By signing in, you agree to our Terms of Service and Privacy Policy.
        </p>
      </div>
    </div>
  );
}
