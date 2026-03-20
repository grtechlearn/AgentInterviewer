'use client';

import Link from 'next/link';

const MOCK_REPORT = {
  sessionId: 'session-001',
  domain: 'Python',
  difficulty: 'Medium',
  totalScore: 38,
  maxScore: 50,
  percentage: 76,
  questions: [
    { id: '1', text: 'Explain the difference between a list and a tuple in Python.', score: 9, maxScore: 10, feedback: 'Excellent explanation with clear examples.' },
    { id: '2', text: 'What is a decorator in Python and how would you use one?', score: 7, maxScore: 10, feedback: 'Good understanding but missed advanced use cases like decorator factories.' },
    { id: '3', text: 'Explain how garbage collection works in Python.', score: 6, maxScore: 10, feedback: 'Covered reference counting but missed generational GC details.' },
    { id: '4', text: 'What are Python generators and when would you use them?', score: 8, maxScore: 10, feedback: 'Strong answer with practical examples of lazy evaluation.' },
    { id: '5', text: 'Describe the Global Interpreter Lock (GIL) and its implications.', score: 8, maxScore: 10, feedback: 'Well-explained with good coverage of multi-threading limitations.' },
  ],
  strengths: [
    'Strong understanding of Python data structures',
    'Good practical knowledge of generators and iterators',
    'Clear communication of complex concepts',
  ],
  weaknesses: [
    'Memory management concepts need more depth',
    'Decorator advanced patterns could be improved',
    'Should practice more system-level Python topics',
  ],
  studyPlan: [
    'Review Python memory management and garbage collection in depth',
    'Practice implementing decorator factories and class decorators',
    'Study Python concurrency: threading, multiprocessing, and asyncio',
    'Complete 5 more medium-difficulty Python interviews this week',
  ],
};

export default function ResultsPage() {
  const report = MOCK_REPORT;

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      {/* Header */}
      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Interview Results</h1>
        <p className="text-gray-500">{report.domain} &middot; {report.difficulty} &middot; {report.questions.length} questions</p>
      </div>

      {/* Overall Score */}
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 text-center mb-8">
        <div className={`text-7xl font-extrabold mb-3 ${
          report.percentage >= 80 ? 'text-green-500' : report.percentage >= 60 ? 'text-yellow-500' : 'text-red-500'
        }`}>
          {report.percentage}%
        </div>
        <p className="text-gray-500 text-lg">Score: {report.totalScore} / {report.maxScore}</p>
        <div className="mt-4 flex justify-center gap-3">
          <button className="px-5 py-2 bg-blue-50 text-blue-600 rounded-lg text-sm font-medium hover:bg-blue-100 transition-colors">
            Share Results
          </button>
          <button className="px-5 py-2 bg-gray-50 text-gray-600 rounded-lg text-sm font-medium hover:bg-gray-100 transition-colors">
            Download PDF
          </button>
        </div>
      </div>

      {/* Per-Question Breakdown */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Question Breakdown</h2>
        <div className="space-y-4">
          {report.questions.map((q, i) => (
            <div key={q.id} className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
              <div className="flex items-start justify-between mb-3">
                <h3 className="font-medium text-gray-900 pr-4">
                  <span className="text-blue-500 mr-2">Q{i + 1}.</span>
                  {q.text}
                </h3>
                <span className={`flex-shrink-0 text-sm font-bold px-3 py-1 rounded-full ${
                  q.score >= 8 ? 'bg-green-100 text-green-700' :
                  q.score >= 6 ? 'bg-yellow-100 text-yellow-700' :
                  'bg-red-100 text-red-700'
                }`}>
                  {q.score}/{q.maxScore}
                </span>
              </div>
              <p className="text-sm text-gray-500">{q.feedback}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Strengths & Weaknesses */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-green-50 rounded-xl p-6">
          <h2 className="text-lg font-semibold text-green-800 mb-3">Strengths</h2>
          <ul className="space-y-2">
            {report.strengths.map((s, i) => (
              <li key={i} className="text-sm text-green-700 flex items-start gap-2">
                <span className="mt-0.5">+</span>
                {s}
              </li>
            ))}
          </ul>
        </div>
        <div className="bg-red-50 rounded-xl p-6">
          <h2 className="text-lg font-semibold text-red-800 mb-3">Areas to Improve</h2>
          <ul className="space-y-2">
            {report.weaknesses.map((w, i) => (
              <li key={i} className="text-sm text-red-700 flex items-start gap-2">
                <span className="mt-0.5">-</span>
                {w}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Study Plan */}
      <div className="bg-blue-50 rounded-xl p-6 mb-8">
        <h2 className="text-lg font-semibold text-blue-800 mb-3">Recommended Study Plan</h2>
        <ol className="space-y-2">
          {report.studyPlan.map((item, i) => (
            <li key={i} className="text-sm text-blue-700 flex items-start gap-3">
              <span className="flex-shrink-0 w-6 h-6 bg-blue-200 rounded-full flex items-center justify-center text-xs font-bold text-blue-800">
                {i + 1}
              </span>
              {item}
            </li>
          ))}
        </ol>
      </div>

      {/* Actions */}
      <div className="text-center">
        <Link
          href="/interview"
          className="inline-flex px-8 py-3 bg-blue-500 text-white font-semibold rounded-xl hover:bg-blue-600 transition-colors"
        >
          Start New Interview
        </Link>
      </div>
    </div>
  );
}
