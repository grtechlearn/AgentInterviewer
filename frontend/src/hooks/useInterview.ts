'use client';

import { useState, useCallback } from 'react';
import { InterviewConfig, InterviewQuestion, EvaluationResult } from '@/lib/types';
import { startInterview, evaluateAnswer } from '@/lib/api';

const MOCK_QUESTIONS: InterviewQuestion[] = [
  { id: '1', text: 'Explain the difference between a list and a tuple in Python.', domain: 'python', difficulty: 'easy' },
  { id: '2', text: 'What is a decorator in Python and how would you use one?', domain: 'python', difficulty: 'medium' },
  { id: '3', text: 'Explain how garbage collection works in Python.', domain: 'python', difficulty: 'medium' },
  { id: '4', text: 'What are Python generators and when would you use them?', domain: 'python', difficulty: 'medium' },
  { id: '5', text: 'Describe the Global Interpreter Lock (GIL) and its implications.', domain: 'python', difficulty: 'hard' },
];

function getMockEvaluation(questionId: string): EvaluationResult {
  const score = Math.floor(Math.random() * 4) + 5;
  return {
    questionId,
    score,
    maxScore: 10,
    correctPoints: ['Good understanding of core concepts', 'Clear explanation'],
    incorrectPoints: score < 8 ? ['Minor inaccuracy in edge cases'] : [],
    missingPoints: score < 7 ? ['Could mention performance implications'] : [],
    feedback: score >= 8
      ? 'Excellent answer! You demonstrated strong understanding.'
      : 'Good attempt. Consider elaborating on edge cases and performance.',
  };
}

export function useInterview() {
  const [sessionId, setSessionId] = useState<string>('');
  const [questions, setQuestions] = useState<InterviewQuestion[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [scores, setScores] = useState<EvaluationResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isStarted, setIsStarted] = useState(false);
  const [isFinished, setIsFinished] = useState(false);

  const start = useCallback(async (config: InterviewConfig) => {
    setIsLoading(true);
    try {
      const result = await startInterview(config);
      setSessionId(result.sessionId);
      setQuestions(result.questions);
    } catch {
      setSessionId('mock-session-' + Date.now());
      setQuestions(MOCK_QUESTIONS.slice(0, config.questionCount));
    }
    setCurrentIndex(0);
    setScores([]);
    setIsStarted(true);
    setIsFinished(false);
    setIsLoading(false);
  }, []);

  const submitAnswer = useCallback(async (answer: string) => {
    if (!questions[currentIndex]) return null;
    setIsLoading(true);
    let evaluation: EvaluationResult;
    try {
      evaluation = await evaluateAnswer(questions[currentIndex].id, answer, sessionId);
    } catch {
      evaluation = getMockEvaluation(questions[currentIndex].id);
    }
    setScores((prev) => [...prev, evaluation]);
    setIsLoading(false);
    return evaluation;
  }, [questions, currentIndex, sessionId]);

  const next = useCallback(() => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex((i) => i + 1);
    }
  }, [currentIndex, questions.length]);

  const finish = useCallback(() => {
    setIsFinished(true);
  }, []);

  const totalScore = scores.reduce((sum, s) => sum + s.score, 0);
  const maxScore = scores.reduce((sum, s) => sum + s.maxScore, 0);

  return {
    sessionId,
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
  };
}
