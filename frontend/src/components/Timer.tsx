'use client';

import { useState, useEffect } from 'react';

interface Props {
  seconds: number;
  onComplete?: () => void;
}

export default function Timer({ seconds: initialSeconds, onComplete }: Props) {
  const [seconds, setSeconds] = useState(initialSeconds);

  useEffect(() => {
    setSeconds(initialSeconds);
  }, [initialSeconds]);

  useEffect(() => {
    if (seconds <= 0) {
      onComplete?.();
      return;
    }
    const timer = setInterval(() => {
      setSeconds((s) => s - 1);
    }, 1000);
    return () => clearInterval(timer);
  }, [seconds, onComplete]);

  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  const display = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;

  const isWarning = seconds < 30;
  const isCritical = seconds < 10;

  return (
    <div
      className={`font-mono text-lg font-semibold px-4 py-1.5 rounded-lg transition-colors ${
        isCritical
          ? 'text-red-600 bg-red-50 animate-pulse'
          : isWarning
          ? 'text-red-500 bg-red-50'
          : 'text-gray-600 bg-gray-50'
      }`}
    >
      {display}
    </div>
  );
}
