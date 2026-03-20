'use client';

import { useState } from 'react';
import { useInterview } from '@/hooks/useInterview';
import InterviewSetup from '@/components/InterviewSetup';
import ScoreCard from '@/components/ScoreCard';
import Timer from '@/components/Timer';
import { InterviewConfig, EvaluationResult } from '@/lib/types';

export default function InterviewPage() {
  const {
    questions,
    currentIndex,
    scores,
    isLoading,
    isStarted,
    isFinished,
    totalScore,
    maxScore,
    start,
    submitAnswer,
    next,
    finish,
  } = useInterview();

  const [answer, setAnswer] = useState('');
  const [lastEvaluation, setLastEvaluation] = useState<EvaluationResult | null>(null);
  const [showScore, setShowScore] = useState(false);

  const handleStart = (config: InterviewConfig) => {
    start(config);
  };

  const handleSubmit = async () => {
    if (!answer.trim()) return;
    const evaluation = await submitAnswer(answer);
    if (evaluation) {
      setLastEvaluation(evaluation);
      setShowScore(true);
    }
  };

  const handleNext = () => {
    setAnswer('');
    setShowScore(false);
    setLastEvaluation(null);
    if (currentIndex < questions.length - 1) {
      next();
    } else {
      finish();
    }
  };

  // Setup screen
  if (!isStarted) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Start Interview</h1>
        <p className="text-gray-500 mb-8">Configure your practice session and begin.</p>
        <InterviewSetup onStart={handleStart} />
      </div>
    );
  }

  // Results screen
  if (isFinished) {
    const percentage = maxScore > 0 ? Math.round((totalScore / maxScore) * 100) : 0;
    return (
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Interview Complete!</h1>
          <p className="text-gray-500">Here&apos;s your performance summary.</p>
        </div>

        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 text-center mb-8">
          <div className={`text-6xl font-extrabold mb-2 ${
            percentage >= 80 ? 'text-green-500' : percentage >= 60 ? 'text-yellow-500' : 'text-red-500'
          }`}>
            {percentage}%
          </div>
          <p className="text-gray-500">Overall Score: {totalScore} / {maxScore}</p>
        </div>

        <div className="space-y-4">
          {questions.map((q, i) => (
            <div key={q.id} className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
              <div className="flex items-start justify-between mb-2">
                <h3 className="font-semibold text-gray-900">Q{i + 1}: {q.text}</h3>
                {scores[i] && (
                  <span className={`text-sm font-bold px-3 py-1 rounded-full ${
                    scores[i].score >= 8 ? 'bg-green-100 text-green-700' :
                    scores[i].score >= 6 ? 'bg-yellow-100 text-yellow-700' :
                    'bg-red-100 text-red-700'
                  }`}>
                    {scores[i].score}/{scores[i].maxScore}
                  </span>
                )}
              </div>
              {scores[i] && <p className="text-sm text-gray-500">{scores[i].feedback}</p>}
            </div>
          ))}
        </div>

        <div className="mt-8 text-center">
          <button
            onClick={() => window.location.reload()}
            className="px-8 py-3 bg-blue-500 text-white font-semibold rounded-xl hover:bg-blue-600 transition-colors"
          >
            Start New Interview
          </button>
        </div>
      </div>
    );
  }

  // Active interview
  const currentQuestion = questions[currentIndex];
  const progress = ((currentIndex + 1) / questions.length) * 100;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <span className="text-sm text-gray-400 font-medium">
            Question {currentIndex + 1} of {questions.length}
          </span>
        </div>
        <Timer seconds={300} />
      </div>

      {/* Progress Bar */}
      <div className="w-full h-2 bg-gray-100 rounded-full mb-8 overflow-hidden">
        <div
          className="h-full bg-blue-500 rounded-full transition-all duration-500"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Question */}
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 mb-6">
        <div className="flex items-center gap-2 mb-4">
          <span className="px-3 py-1 bg-blue-50 text-blue-600 text-xs font-semibold rounded-full uppercase">
            {currentQuestion?.domain}
          </span>
          <span className="px-3 py-1 bg-gray-50 text-gray-500 text-xs font-semibold rounded-full uppercase">
            {currentQuestion?.difficulty}
          </span>
        </div>
        <h2 className="text-xl font-semibold text-gray-900">{currentQuestion?.text}</h2>
      </div>

      {/* Answer / Score */}
      {showScore && lastEvaluation ? (
        <div className="mb-6">
          <ScoreCard evaluation={lastEvaluation} />
          <div className="mt-6 text-center">
            <button
              onClick={handleNext}
              className="px-8 py-3 bg-blue-500 text-white font-semibold rounded-xl hover:bg-blue-600 transition-colors"
            >
              {currentIndex < questions.length - 1 ? 'Next Question' : 'View Results'}
            </button>
          </div>
        </div>
      ) : (
        <div>
          <textarea
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            placeholder="Type your answer here..."
            className="w-full h-48 p-4 font-mono text-sm bg-slate-50 border border-gray-200 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-400 transition-colors"
          />
          <div className="mt-4 flex justify-end">
            <button
              onClick={handleSubmit}
              disabled={isLoading || !answer.trim()}
              className="px-8 py-3 bg-blue-500 text-white font-semibold rounded-xl hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {isLoading ? (
                <>
                  <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" /><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
                  Evaluating...
                </>
              ) : (
                'Submit Answer'
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
