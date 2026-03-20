'use client';

import { useState, useEffect, useCallback, useRef } from 'react';

export interface IntegrityState {
  integrityScore: number;
  tabSwitches: number;
  pasteEvents: number;
  avgResponseTime: number;
  flags: string[];
}

const INITIAL_SCORE = 100;
const TAB_SWITCH_PENALTY = 5;
const PASTE_PENALTY = 10;
const FAST_RESPONSE_PENALTY = 15;
const FAST_RESPONSE_THRESHOLD = 5; // seconds

export function useIntegrity() {
  const [tabSwitches, setTabSwitches] = useState(0);
  const [pasteEvents, setPasteEvents] = useState(0);
  const [responseTimes, setResponseTimes] = useState<number[]>([]);
  const [flags, setFlags] = useState<string[]>([]);
  const questionShownAt = useRef<number>(Date.now());

  // Track tab visibility changes
  useEffect(() => {
    const handleVisibility = () => {
      if (document.hidden) {
        setTabSwitches((prev) => {
          const next = prev + 1;
          setFlags((f) => [...f, `Tab switch #${next} at ${new Date().toLocaleTimeString()}`]);
          return next;
        });
      }
    };
    document.addEventListener('visibilitychange', handleVisibility);
    return () => document.removeEventListener('visibilitychange', handleVisibility);
  }, []);

  // Track paste events
  useEffect(() => {
    const handlePaste = () => {
      setPasteEvents((prev) => {
        const next = prev + 1;
        setFlags((f) => [...f, `Paste event #${next} at ${new Date().toLocaleTimeString()}`]);
        return next;
      });
    };
    document.addEventListener('paste', handlePaste);
    return () => document.removeEventListener('paste', handlePaste);
  }, []);

  // Call when a new question is shown
  const markQuestionShown = useCallback(() => {
    questionShownAt.current = Date.now();
  }, []);

  // Call when an answer is submitted; returns elapsed seconds
  const markAnswerSubmitted = useCallback(() => {
    const elapsed = (Date.now() - questionShownAt.current) / 1000;
    setResponseTimes((prev) => {
      const next = [...prev, elapsed];
      return next;
    });
    if (elapsed < FAST_RESPONSE_THRESHOLD) {
      setFlags((f) => [...f, `Fast response (${elapsed.toFixed(1)}s) at ${new Date().toLocaleTimeString()}`]);
    }
    return elapsed;
  }, []);

  // Calculate scores
  const fastResponses = responseTimes.filter((t) => t < FAST_RESPONSE_THRESHOLD).length;
  const integrityScore = Math.max(
    0,
    INITIAL_SCORE -
      tabSwitches * TAB_SWITCH_PENALTY -
      pasteEvents * PASTE_PENALTY -
      fastResponses * FAST_RESPONSE_PENALTY,
  );

  const avgResponseTime =
    responseTimes.length > 0
      ? responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length
      : 0;

  return {
    integrityScore,
    tabSwitches,
    pasteEvents,
    avgResponseTime,
    flags,
    markQuestionShown,
    markAnswerSubmitted,
  };
}
