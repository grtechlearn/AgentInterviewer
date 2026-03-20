'use client';

import { useState, useCallback } from 'react';
import Timer from '@/components/Timer';
import { QuizQuestion } from '@/lib/types';

const DOMAIN_OPTIONS = ['Python', 'React', 'iOS', 'Android', 'Java', 'DevOps', 'System Design', 'HR'];

const MOCK_QUIZ: QuizQuestion[] = [
  {
    id: '1', domain: 'python',
    text: 'Which of the following is immutable in Python?',
    options: ['List', 'Dictionary', 'Tuple', 'Set'],
    correctIndex: 2,
    explanation: 'Tuples are immutable sequences in Python. Once created, their elements cannot be changed.',
  },
  {
    id: '2', domain: 'python',
    text: 'What does the "yield" keyword do in Python?',
    options: ['Stops execution', 'Creates a generator', 'Returns a value permanently', 'Raises an exception'],
    correctIndex: 1,
    explanation: 'The yield keyword turns a function into a generator, which produces values lazily one at a time.',
  },
  {
    id: '3', domain: 'python',
    text: 'What is the time complexity of dictionary lookup in Python?',
    options: ['O(n)', 'O(log n)', 'O(1) average', 'O(n log n)'],
    correctIndex: 2,
    explanation: 'Python dictionaries use hash tables, providing O(1) average time complexity for lookups.',
  },
  {
    id: '4', domain: 'python',
    text: 'Which statement about Python\'s GIL is correct?',
    options: ['It allows true multi-threading', 'It prevents parallel CPU-bound threads', 'It only affects I/O operations', 'It was removed in Python 3'],
    correctIndex: 1,
    explanation: 'The Global Interpreter Lock prevents multiple threads from executing Python bytecode simultaneously, limiting CPU-bound parallelism.',
  },
  {
    id: '5', domain: 'python',
    text: 'What is a Python decorator?',
    options: ['A design pattern only', 'A function that modifies another function', 'A class attribute', 'A type annotation'],
    correctIndex: 1,
    explanation: 'A decorator is a function that takes another function as input and extends its behavior without modifying it.',
  },
];

export default function QuizPage() {
  const [selectedDomain, setSelectedDomain] = useState('');
  const [isStarted, setIsStarted] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [isAnswered, setIsAnswered] = useState(false);
  const [correctCount, setCorrectCount] = useState(0);
  const [isFinished, setIsFinished] = useState(false);
  const [questions] = useState<QuizQuestion[]>(MOCK_QUIZ);

  const handleStart = () => {
    if (!selectedDomain) return;
    setIsStarted(true);
    setCurrentIndex(0);
    setCorrectCount(0);
    setIsFinished(false);
  };

  const handleSelect = (index: number) => {
    if (isAnswered) return;
    setSelectedOption(index);
    setIsAnswered(true);
    if (index === questions[currentIndex].correctIndex) {
      setCorrectCount((c) => c + 1);
    }
  };

  const handleNext = useCallback(() => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex((i) => i + 1);
      setSelectedOption(null);
      setIsAnswered(false);
    } else {
      setIsFinished(true);
    }
  }, [currentIndex, questions.length]);

  // Domain selector
  if (!isStarted) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Quick Quiz</h1>
        <p className="text-gray-500 mb-8">Test your knowledge with multiple choice questions.</p>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
          {DOMAIN_OPTIONS.map((domain) => (
            <button
              key={domain}
              onClick={() => setSelectedDomain(domain)}
              className={`p-4 rounded-xl border text-sm font-medium transition-all ${
                selectedDomain === domain
                  ? 'bg-blue-50 border-blue-300 text-blue-600'
                  : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'
              }`}
            >
              {domain}
            </button>
          ))}
        </div>
        <button
          onClick={handleStart}
          disabled={!selectedDomain}
          className="px-8 py-3 bg-blue-500 text-white font-semibold rounded-xl hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Start Quiz
        </button>
      </div>
    );
  }

  // Results
  if (isFinished) {
    const percentage = Math.round((correctCount / questions.length) * 100);
    return (
      <div className="max-w-3xl mx-auto px-4 py-12 text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Quiz Complete!</h1>
        <div className={`text-6xl font-extrabold mb-2 ${
          percentage >= 80 ? 'text-green-500' : percentage >= 60 ? 'text-yellow-500' : 'text-red-500'
        }`}>
          {percentage}%
        </div>
        <p className="text-gray-500 mb-8">{correctCount} out of {questions.length} correct</p>
        <button
          onClick={() => { setIsStarted(false); setSelectedDomain(''); }}
          className="px-8 py-3 bg-blue-500 text-white font-semibold rounded-xl hover:bg-blue-600 transition-colors"
        >
          Try Again
        </button>
      </div>
    );
  }

  // Active quiz
  const q = questions[currentIndex];

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <span className="text-sm text-gray-400 font-medium">
          Question {currentIndex + 1} of {questions.length}
        </span>
        <Timer seconds={30} />
      </div>

      {/* Progress */}
      <div className="w-full h-2 bg-gray-100 rounded-full mb-8 overflow-hidden">
        <div
          className="h-full bg-blue-500 rounded-full transition-all duration-500"
          style={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }}
        />
      </div>

      {/* Question */}
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-6">{q.text}</h2>
        <div className="space-y-3">
          {q.options.map((option, i) => {
            let style = 'bg-white border-gray-200 text-gray-700 hover:bg-gray-50';
            if (isAnswered) {
              if (i === q.correctIndex) {
                style = 'bg-green-50 border-green-300 text-green-700';
              } else if (i === selectedOption && i !== q.correctIndex) {
                style = 'bg-red-50 border-red-300 text-red-700';
              } else {
                style = 'bg-gray-50 border-gray-100 text-gray-400';
              }
            } else if (i === selectedOption) {
              style = 'bg-blue-50 border-blue-300 text-blue-600';
            }
            return (
              <button
                key={i}
                onClick={() => handleSelect(i)}
                disabled={isAnswered}
                className={`w-full text-left p-4 rounded-xl border font-medium transition-all ${style}`}
              >
                <span className="mr-3 text-sm opacity-60">{String.fromCharCode(65 + i)}.</span>
                {option}
              </button>
            );
          })}
        </div>
      </div>

      {/* Explanation */}
      {isAnswered && (
        <div className="bg-blue-50 rounded-xl p-6 mb-6">
          <p className="text-sm text-blue-800 font-medium mb-1">Explanation</p>
          <p className="text-sm text-blue-700">{q.explanation}</p>
        </div>
      )}

      {isAnswered && (
        <div className="text-center">
          <button
            onClick={handleNext}
            className="px-8 py-3 bg-blue-500 text-white font-semibold rounded-xl hover:bg-blue-600 transition-colors"
          >
            {currentIndex < questions.length - 1 ? 'Next Question' : 'View Results'}
          </button>
        </div>
      )}
    </div>
  );
}
