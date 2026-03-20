'use client';

import { useState, useEffect } from 'react';
import { useInterview } from '@/hooks/useInterview';
import { useIntegrity } from '@/hooks/useIntegrity';
import InterviewSetup from '@/components/InterviewSetup';
import ScoreCard from '@/components/ScoreCard';
import Timer from '@/components/Timer';
import { InterviewConfig, EvaluationResult } from '@/lib/types';

export default function InterviewPage() {
  const { questions, currentIndex, scores, isLoading, isStarted, isFinished,
    totalScore, maxScore, start, submitAnswer, next, finish } = useInterview();
  const integrity = useIntegrity();
  const [answer, setAnswer] = useState('');
  const [lastEvaluation, setLastEvaluation] = useState<EvaluationResult | null>(null);
  const [showScore, setShowScore] = useState(false);

  useEffect(() => {
    if (isStarted && !isFinished) integrity.markQuestionShown();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentIndex, isStarted, isFinished]);

  const handleStart = (config: InterviewConfig) => start(config);

  const handleSubmit = async () => {
    if (!answer.trim()) return;
    integrity.markAnswerSubmitted();
    const evaluation = await submitAnswer(answer);
    if (evaluation) { setLastEvaluation(evaluation); setShowScore(true); }
  };

  const handleNext = () => {
    setAnswer(''); setShowScore(false); setLastEvaluation(null);
    currentIndex < questions.length - 1 ? next() : finish();
  };

  if (!isStarted) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Start Interview</h1>
        <p className="text-gray-500 dark:text-gray-400 mb-8">Configure your practice session and begin.</p>
        <InterviewSetup onStart={handleStart} />
      </div>
    );
  }

  if (isFinished) {
    const pct = maxScore > 0 ? Math.round((totalScore / maxScore) * 100) : 0;
    const color = pct >= 80 ? 'text-green-500' : pct >= 60 ? 'text-yellow-500' : 'text-red-500';
    return (
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Interview Complete!</h1>
          <p className="text-gray-500 dark:text-gray-400">Here&apos;s your performance summary.</p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm p-8 text-center mb-8">
          <div className={`text-6xl font-extrabold mb-2 ${color}`}>{pct}%</div>
          <p className="text-gray-500 dark:text-gray-400">Overall Score: {totalScore} / {maxScore}</p>
          <p className="text-sm mt-2 text-gray-400 dark:text-gray-500">Integrity Score: {integrity.integrityScore}/100</p>
        </div>
        <div className="space-y-4">
          {questions.map((q, i) => {
            const s = scores[i];
            const badge = s ? (s.score >= 8 ? 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300'
              : s.score >= 6 ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300'
              : 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300') : '';
            return (
              <div key={q.id} className="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 shadow-sm p-6">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="font-semibold text-gray-900 dark:text-white">Q{i + 1}: {q.text}</h3>
                  {s && <span className={`text-sm font-bold px-3 py-1 rounded-full ${badge}`}>{s.score}/{s.maxScore}</span>}
                </div>
                {s && <p className="text-sm text-gray-500 dark:text-gray-400">{s.feedback}</p>}
              </div>
            );
          })}
        </div>
        <div className="mt-8 text-center">
          <button onClick={() => window.location.reload()} className="px-8 py-3 bg-blue-500 text-white font-semibold rounded-xl hover:bg-blue-600 transition-colors">
            Start New Interview
          </button>
        </div>
      </div>
    );
  }

  const currentQuestion = questions[currentIndex];
  const progress = ((currentIndex + 1) / questions.length) * 100;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {integrity.integrityScore < 70 && (
        <div className="mb-4 p-4 bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-xl">
          <p className="text-sm font-medium text-red-700 dark:text-red-300">
            Integrity Warning: Your integrity score is {integrity.integrityScore}/100. Avoid switching tabs or pasting content.
          </p>
        </div>
      )}
      <div className="flex items-center justify-between mb-6">
        <span className="text-sm text-gray-400 dark:text-gray-500 font-medium">Question {currentIndex + 1} of {questions.length}</span>
        <div className="flex items-center gap-4">
          <span className="text-xs text-gray-400 dark:text-gray-500">Integrity: {integrity.integrityScore}%</span>
          <Timer seconds={300} />
        </div>
      </div>
      <div className="w-full h-2 bg-gray-100 dark:bg-gray-700 rounded-full mb-8 overflow-hidden">
        <div className="h-full bg-blue-500 rounded-full transition-all duration-500" style={{ width: `${progress}%` }} />
      </div>
      <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm p-8 mb-6">
        <div className="flex items-center gap-2 mb-4">
          <span className="px-3 py-1 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 text-xs font-semibold rounded-full uppercase">{currentQuestion?.domain}</span>
          <span className="px-3 py-1 bg-gray-50 dark:bg-gray-700 text-gray-500 dark:text-gray-400 text-xs font-semibold rounded-full uppercase">{currentQuestion?.difficulty}</span>
        </div>
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">{currentQuestion?.text}</h2>
      </div>
      {showScore && lastEvaluation ? (
        <div className="mb-6">
          <ScoreCard evaluation={lastEvaluation} />
          <div className="mt-6 text-center">
            <button onClick={handleNext} className="px-8 py-3 bg-blue-500 text-white font-semibold rounded-xl hover:bg-blue-600 transition-colors">
              {currentIndex < questions.length - 1 ? 'Next Question' : 'View Results'}
            </button>
          </div>
        </div>
      ) : (
        <div>
          <textarea value={answer} onChange={(e) => setAnswer(e.target.value)} placeholder="Type your answer here..."
            className="w-full h-48 p-4 font-mono text-sm bg-slate-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-400 transition-colors text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500" />
          <div className="mt-4 flex justify-end">
            <button onClick={handleSubmit} disabled={isLoading || !answer.trim()}
              className="px-8 py-3 bg-blue-500 text-white font-semibold rounded-xl hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2">
              {isLoading ? (
                <><svg className="animate-spin h-4 w-4" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" /><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>Evaluating...</>
              ) : 'Submit Answer'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
