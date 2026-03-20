export interface InterviewQuestion {
  id: string;
  text: string;
  domain: string;
  difficulty: 'easy' | 'medium' | 'hard';
  expectedAnswer?: string;
  hints?: string[];
  timeLimit?: number;
}

export interface EvaluationResult {
  questionId: string;
  score: number;
  maxScore: number;
  correctPoints: string[];
  incorrectPoints: string[];
  missingPoints: string[];
  feedback: string;
}

export interface SessionReport {
  sessionId: string;
  domain: string;
  difficulty: string;
  totalScore: number;
  maxScore: number;
  percentage: number;
  questions: InterviewQuestion[];
  evaluations: EvaluationResult[];
  strengths: string[];
  weaknesses: string[];
  studyPlan: string[];
  timestamp: string;
}

export interface UserStats {
  userId: string;
  xp: number;
  level: number;
  streak: number;
  title: string;
  totalInterviews: number;
  avgScore: number;
  skills: Record<string, SkillLevel>;
  achievements: Achievement[];
}

export interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  unlockedAt?: string;
  progress: number;
  target: number;
}

export interface Goal {
  id: string;
  title: string;
  description: string;
  targetDate: string;
  progress: number;
  target: number;
  domain: string;
}

export interface SkillLevel {
  domain: string;
  level: number;
  maxLevel: number;
  score: number;
  questionsAnswered: number;
}

export interface QuizQuestion {
  id: string;
  text: string;
  options: string[];
  correctIndex: number;
  explanation: string;
  domain: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface InterviewConfig {
  domain: string;
  difficulty: 'easy' | 'medium' | 'hard';
  questionCount: number;
  userId?: string;
}
