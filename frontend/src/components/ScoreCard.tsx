'use client';

import { EvaluationResult } from '@/lib/types';

interface Props {
  evaluation: EvaluationResult;
}

export default function ScoreCard({ evaluation }: Props) {
  const { score, maxScore, correctPoints, incorrectPoints, missingPoints, feedback } = evaluation;
  const percentage = Math.round((score / maxScore) * 100);

  const scoreColor = percentage >= 80 ? 'text-green-500' : percentage >= 60 ? 'text-yellow-500' : 'text-red-500';
  const bgColor = percentage >= 80 ? 'bg-green-50' : percentage >= 60 ? 'bg-yellow-50' : 'bg-red-50';

  return (
    <div className={`rounded-2xl p-6 ${bgColor}`}>
      {/* Score */}
      <div className="text-center mb-5">
        <div className={`text-5xl font-extrabold ${scoreColor}`}>
          {score}<span className="text-2xl text-gray-400">/{maxScore}</span>
        </div>
      </div>

      {/* Points Breakdown */}
      <div className="space-y-3 mb-5">
        {correctPoints.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {correctPoints.map((point, i) => (
              <span key={i} className="inline-flex items-center gap-1 px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
                <span>+</span> {point}
              </span>
            ))}
          </div>
        )}
        {incorrectPoints.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {incorrectPoints.map((point, i) => (
              <span key={i} className="inline-flex items-center gap-1 px-3 py-1 bg-red-100 text-red-700 rounded-full text-xs font-medium">
                <span>-</span> {point}
              </span>
            ))}
          </div>
        )}
        {missingPoints.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {missingPoints.map((point, i) => (
              <span key={i} className="inline-flex items-center gap-1 px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-xs font-medium">
                <span>?</span> {point}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Feedback */}
      <p className="text-sm text-gray-700 leading-relaxed">{feedback}</p>
    </div>
  );
}
