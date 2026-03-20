'use client';

interface Props {
  xp: number;
  level: number;
  nextLevelXp: number;
  progress: number;
}

export default function XPBar({ xp, level, nextLevelXp, progress }: Props) {
  return (
    <div>
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <span className="w-7 h-7 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center text-white text-xs font-bold">
            {level}
          </span>
          <span className="text-sm font-semibold text-gray-700">Level {level}</span>
        </div>
        <span className="text-xs text-gray-400 font-medium">{xp} / {nextLevelXp} XP</span>
      </div>
      <div className="w-full h-3 bg-gray-100 rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full transition-all duration-700"
          style={{ width: `${Math.min(progress * 100, 100)}%` }}
        />
      </div>
    </div>
  );
}
