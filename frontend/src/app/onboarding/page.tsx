'use client';

import { useState } from 'react';
import Link from 'next/link';

const STEPS = ['Goal', 'Stack', 'Level', 'Target', 'Assessment'];

const GOAL_OPTIONS = ['Campus Placement', 'Job Switch', 'FAANG Prep', 'Freelance', 'Upskilling'];
const STACK_OPTIONS = ['Python', 'JavaScript', 'React', 'Java', 'Node.js', 'Go', 'Swift', 'Kotlin', 'DevOps', 'SQL'];
const LEVEL_OPTIONS = ['Beginner (0-1 yrs)', 'Intermediate (1-3 yrs)', 'Senior (3-5 yrs)', 'Expert (5+ yrs)'];
const TARGET_OPTIONS = ['1-2 interviews/week', '3-5 interviews/week', 'Daily practice', 'Weekend only'];
const ASSESS_OPTIONS = ['Data Structures', 'Algorithms', 'System Design', 'Frontend', 'Backend', 'Database', 'Networking'];

export default function OnboardingPage() {
  const [step, setStep] = useState(0);
  const [goal, setGoal] = useState('');
  const [stack, setStack] = useState<string[]>([]);
  const [level, setLevel] = useState('');
  const [target, setTarget] = useState('');
  const [assess, setAssess] = useState<string[]>([]);

  const toggleStack = (s: string) => setStack((prev) => prev.includes(s) ? prev.filter((x) => x !== s) : [...prev, s]);
  const toggleAssess = (a: string) => setAssess((prev) => prev.includes(a) ? prev.filter((x) => x !== a) : [...prev, a]);

  const canNext = [goal, stack.length > 0, level, target, assess.length > 0][step];

  return (
    <div className="min-h-[calc(100vh-4rem)] flex flex-col items-center px-4 py-12 bg-slate-50">
      {/* Step Indicator */}
      <div className="flex items-center gap-2 mb-10">
        {STEPS.map((s, i) => (
          <div key={s} className="flex items-center gap-2">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
              i < step ? 'bg-blue-500 text-white' : i === step ? 'bg-blue-500 text-white ring-4 ring-blue-100' : 'bg-gray-200 text-gray-500'
            }`}>
              {i < step ? '✓' : i + 1}
            </div>
            <span className={`text-xs font-medium hidden sm:block ${i === step ? 'text-blue-500' : 'text-gray-400'}`}>{s}</span>
            {i < STEPS.length - 1 && <div className={`w-8 h-0.5 ${i < step ? 'bg-blue-500' : 'bg-gray-200'}`} />}
          </div>
        ))}
      </div>

      <div className="w-full max-w-lg bg-white rounded-xl border border-gray-100 shadow-sm p-8">
        {/* Step 1: Goal */}
        {step === 0 && (
          <div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">What&apos;s your goal?</h2>
            <p className="text-sm text-gray-500 mb-6">Choose your primary interview preparation goal.</p>
            <div className="space-y-3">
              {GOAL_OPTIONS.map((g) => (
                <button key={g} onClick={() => setGoal(g)} className={`w-full text-left px-4 py-3 rounded-xl border text-sm font-medium transition-colors ${
                  goal === g ? 'border-blue-500 bg-blue-50 text-blue-700' : 'border-gray-200 text-gray-700 hover:bg-gray-50'
                }`}>{g}</button>
              ))}
            </div>
          </div>
        )}

        {/* Step 2: Stack */}
        {step === 1 && (
          <div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">Select your tech stack</h2>
            <p className="text-sm text-gray-500 mb-6">Pick all technologies you want to practice.</p>
            <div className="flex flex-wrap gap-2">
              {STACK_OPTIONS.map((s) => (
                <button key={s} onClick={() => toggleStack(s)} className={`px-4 py-2 rounded-lg text-sm font-medium border transition-colors ${
                  stack.includes(s) ? 'border-blue-500 bg-blue-50 text-blue-700' : 'border-gray-200 text-gray-600 hover:bg-gray-50'
                }`}>{s}</button>
              ))}
            </div>
          </div>
        )}

        {/* Step 3: Level */}
        {step === 2 && (
          <div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">Your experience level</h2>
            <p className="text-sm text-gray-500 mb-6">We&apos;ll adjust difficulty accordingly.</p>
            <div className="space-y-3">
              {LEVEL_OPTIONS.map((l) => (
                <button key={l} onClick={() => setLevel(l)} className={`w-full text-left px-4 py-3 rounded-xl border text-sm font-medium transition-colors ${
                  level === l ? 'border-blue-500 bg-blue-50 text-blue-700' : 'border-gray-200 text-gray-700 hover:bg-gray-50'
                }`}>{l}</button>
              ))}
            </div>
          </div>
        )}

        {/* Step 4: Target */}
        {step === 3 && (
          <div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">Practice frequency</h2>
            <p className="text-sm text-gray-500 mb-6">How often do you want to practice?</p>
            <div className="space-y-3">
              {TARGET_OPTIONS.map((t) => (
                <button key={t} onClick={() => setTarget(t)} className={`w-full text-left px-4 py-3 rounded-xl border text-sm font-medium transition-colors ${
                  target === t ? 'border-blue-500 bg-blue-50 text-blue-700' : 'border-gray-200 text-gray-700 hover:bg-gray-50'
                }`}>{t}</button>
              ))}
            </div>
          </div>
        )}

        {/* Step 5: Assessment */}
        {step === 4 && (
          <div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">Skill assessment focus</h2>
            <p className="text-sm text-gray-500 mb-6">Select areas for your initial assessment.</p>
            <div className="flex flex-wrap gap-2">
              {ASSESS_OPTIONS.map((a) => (
                <button key={a} onClick={() => toggleAssess(a)} className={`px-4 py-2 rounded-lg text-sm font-medium border transition-colors ${
                  assess.includes(a) ? 'border-blue-500 bg-blue-50 text-blue-700' : 'border-gray-200 text-gray-600 hover:bg-gray-50'
                }`}>{a}</button>
              ))}
            </div>
          </div>
        )}

        {/* Navigation */}
        <div className="flex justify-between mt-8">
          <button
            onClick={() => setStep(Math.max(0, step - 1))}
            disabled={step === 0}
            className="px-5 py-2.5 text-sm font-medium text-gray-600 border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-30 transition-colors"
          >Back</button>
          {step < STEPS.length - 1 ? (
            <button
              onClick={() => setStep(step + 1)}
              disabled={!canNext}
              className="px-5 py-2.5 text-sm font-semibold text-white bg-blue-500 rounded-lg hover:bg-blue-600 disabled:opacity-30 transition-colors"
            >Next</button>
          ) : (
            <Link href="/dashboard" className={`px-5 py-2.5 text-sm font-semibold text-white bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors ${!canNext ? 'opacity-30 pointer-events-none' : ''}`}>
              Get Started
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
