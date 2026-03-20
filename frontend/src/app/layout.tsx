import type { Metadata } from 'next';
import Link from 'next/link';
import './globals.css';

export const metadata: Metadata = {
  title: 'AgentInterviewer - AI Interview Practice',
  description: 'Master your next tech interview with AI-powered practice',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-white text-gray-900 min-h-screen font-sans">
        <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <Link href="/" className="flex items-center gap-2">
                <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">AI</span>
                </div>
                <span className="font-bold text-xl text-gray-900">AgentInterviewer</span>
              </Link>
              <div className="hidden md:flex items-center gap-1">
                <Link href="/" className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-blue-500 rounded-lg hover:bg-blue-50 transition-colors">
                  Home
                </Link>
                <Link href="/interview" className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-blue-500 rounded-lg hover:bg-blue-50 transition-colors">
                  Interview
                </Link>
                <Link href="/dashboard" className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-blue-500 rounded-lg hover:bg-blue-50 transition-colors">
                  Dashboard
                </Link>
                <Link href="/quiz" className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-blue-500 rounded-lg hover:bg-blue-50 transition-colors">
                  Quiz
                </Link>
                <Link href="/chat" className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-blue-500 rounded-lg hover:bg-blue-50 transition-colors">
                  Chat
                </Link>
              </div>
              <button className="px-5 py-2 bg-blue-500 text-white text-sm font-medium rounded-lg hover:bg-blue-600 transition-colors shadow-sm">
                Login
              </button>
            </div>
          </div>
        </nav>
        <main>{children}</main>
      </body>
    </html>
  );
}
