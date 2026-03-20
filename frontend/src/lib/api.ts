import { InterviewConfig, InterviewQuestion, EvaluationResult, SessionReport, SkillLevel, Achievement, QuizQuestion } from './types';

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8081';

async function dispatch(action: string, data?: Record<string, unknown>): Promise<unknown> {
  const res = await fetch(`${BASE_URL}/api/${action}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data || {}),
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function startInterview(config: InterviewConfig): Promise<{ sessionId: string; questions: InterviewQuestion[] }> {
  return dispatch('interview/start', config as unknown as Record<string, unknown>) as Promise<{ sessionId: string; questions: InterviewQuestion[] }>;
}

export async function evaluateAnswer(
  questionId: string,
  answer: string,
  sessionId: string
): Promise<EvaluationResult> {
  return dispatch('interview/evaluate', { questionId, answer, sessionId }) as Promise<EvaluationResult>;
}

export async function generateReport(sessionId: string): Promise<SessionReport> {
  return dispatch('interview/report', { sessionId }) as Promise<SessionReport>;
}

export async function startQuiz(domain: string): Promise<{ questions: QuizQuestion[] }> {
  return dispatch('quiz/start', { domain }) as Promise<{ questions: QuizQuestion[] }>;
}

export async function getSkills(userId: string): Promise<Record<string, SkillLevel>> {
  return dispatch('user/skills', { userId }) as Promise<Record<string, SkillLevel>>;
}

export async function getAchievements(userId: string): Promise<Achievement[]> {
  return dispatch('user/achievements', { userId }) as Promise<Achievement[]>;
}

export { dispatch };
