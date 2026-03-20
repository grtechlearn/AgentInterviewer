'use client';

import { useState } from 'react';
import { UserStats, Achievement, SkillLevel } from '@/lib/types';

const MOCK_SKILLS: Record<string, SkillLevel> = {
  python: { domain: 'Python', level: 7, maxLevel: 10, score: 82, questionsAnswered: 45 },
  react: { domain: 'React', level: 5, maxLevel: 10, score: 68, questionsAnswered: 30 },
  ios: { domain: 'iOS', level: 3, maxLevel: 10, score: 45, questionsAnswered: 15 },
  android: { domain: 'Android', level: 4, maxLevel: 10, score: 55, questionsAnswered: 20 },
  java: { domain: 'Java', level: 6, maxLevel: 10, score: 74, questionsAnswered: 35 },
  devops: { domain: 'DevOps', level: 4, maxLevel: 10, score: 52, questionsAnswered: 18 },
  systemdesign: { domain: 'System Design', level: 5, maxLevel: 10, score: 65, questionsAnswered: 25 },
  hr: { domain: 'HR / Behavioral', level: 6, maxLevel: 10, score: 70, questionsAnswered: 28 },
};

const MOCK_ACHIEVEMENTS: Achievement[] = [
  { id: '1', name: 'First Interview', description: 'Complete your first interview', icon: '🎯', unlockedAt: '2024-01-15', progress: 1, target: 1 },
  { id: '2', name: 'Streak Master', description: 'Maintain a 5-day streak', icon: '🔥', unlockedAt: '2024-02-10', progress: 5, target: 5 },
  { id: '3', name: 'Python Pro', description: 'Score 80%+ in 10 Python interviews', icon: '🐍', progress: 7, target: 10 },
  { id: '4', name: 'Full Stack', description: 'Complete interviews in 5 domains', icon: '🏆', progress: 4, target: 5 },
  { id: '5', name: 'Speed Demon', description: 'Complete an interview in under 10 minutes', icon: '⚡', unlockedAt: '2024-03-01', progress: 1, target: 1 },
  { id: '6', name: 'Perfectionist', description: 'Score 100% on any interview', icon: '💎', progress: 0, target: 1 },
];

const MOCK_USER: UserStats = {
  userId: 'user-1',
  xp: 250,
  level: 3,
  streak: 5,
  title: 'Developer',
  totalInterviews: 24,
  avgScore: 72,
  skills: MOCK_SKILLS,
  achievements: MOCK_ACHIEVEMENTS,
};

export function useUser() {
  const [user] = useState<UserStats>(MOCK_USER);

  const xpForNextLevel = user.level * 100;
  const xpProgress = (user.xp % 100) / 100;

  return {
    user,
    xpForNextLevel,
    xpProgress,
    skills: user.skills,
    achievements: user.achievements,
  };
}
