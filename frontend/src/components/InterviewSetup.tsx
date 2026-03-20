'use client';

import { useState } from 'react';
import { InterviewConfig } from '@/lib/types';

const DOMAINS = [
  { key: 'python', name: 'Python', emoji: '🐍' },
  { key: 'react', name: 'React', emoji: '⚛️' },
  { key: 'ios', name: 'iOS', emoji: '🍎' },
  { key: 'android', name: 'Android', emoji: '🤖' },
  { key: 'java', name: 'Java', emoji: '☕' },
  { key: 'devops', name: 'DevOps', emoji: '🔧' },
  { key: 'systemdesign', name: 'System Design', emoji: '🏗️' },
  { key: 'hr', name: 'HR', emoji: '🤝' },
];

const DIFFICULTIES = [
  { key: 'easy' as const, label: 'Easy', color: 'bg-green-50 border-green-200 text-green-700' },
  { key: 'medium' as const, label: 'Medium', color: 'bg-yellow-50 border-yellow-200 text-yellow-700' },
  { key: 'hard' as const, label: 'Hard', color: 'bg-red-50 border-red-200 text-red-700' },
];

const QUESTION_COUNTS = [5, 10, 15];

interface Props {
  onStart: (config: InterviewConfig) => void;
}

export default function InterviewSetup({ onStart }: Props) {
  const [domain, setDomain] = useState('');
  const [difficulty, setDifficulty] = useState<'easy' | 'medium' | 'hard'>('medium');
  const [questionCount, setQuestionCount] = useState(5);

  const handleStart = () => {
    if (!domain) return;
    onStart({ domain, difficulty, questionCount });
  };

  return (
    <div className="space-y-8">
      {/* Domain Selection */}
      <div>
        <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Select Domain</h3>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {DOMAINS.map((d) => (
            <button
              key={d.key}
              onClick={() => setDomain(d.key)}
              className={`flex flex-col items-center gap-2 p-5 rounded-xl border transition-all hover:-translate-y-0.5 ${
                domain === d.key
                  ? 'bg-blue-50 border-blue-300 shadow-sm'
                  : 'bg-white border-gray-200 hover:bg-gray-50'
              }`}
            >
              <span className="text-3xl">{d.emoji}</span>
              <span className={`text-sm font-medium ${domain === d.key ? 'text-blue-600' : 'text-gray-700'}`}>
                {d.name}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Difficulty */}
      <div>
        <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Difficulty</h3>
        <div className="flex gap-3">
          {DIFFICULTIES.map((d) => (
            <button
              key={d.key}
              onClick={() => setDifficulty(d.key)}
              className={`px-6 py-2.5 rounded-full border text-sm font-medium transition-all ${
                difficulty === d.key ? d.color : 'bg-white border-gray-200 text-gray-500 hover:bg-gray-50'
              }`}
            >
              {d.label}
            </button>
          ))}
        </div>
      </div>

      {/* Question Count */}
      <div>
        <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Questions</h3>
        <div className="flex gap-3">
          {QUESTION_COUNTS.map((count) => (
            <button
              key={count}
              onClick={() => setQuestionCount(count)}
              className={`w-16 py-2.5 rounded-xl border text-sm font-medium transition-all ${
                questionCount === count
                  ? 'bg-blue-50 border-blue-300 text-blue-600'
                  : 'bg-white border-gray-200 text-gray-500 hover:bg-gray-50'
              }`}
            >
              {count}
            </button>
          ))}
        </div>
      </div>

      {/* Start Button */}
      <button
        onClick={handleStart}
        disabled={!domain}
        className="w-full sm:w-auto px-10 py-3.5 bg-blue-500 text-white font-semibold rounded-xl hover:bg-blue-600 transition-colors shadow-lg shadow-blue-500/25 disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none text-lg"
      >
        Start Interview
      </button>
    </div>
  );
}
