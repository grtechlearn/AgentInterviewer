'use client';

interface Props {
  streak: number;
}

export default function StreakCounter({ streak }: Props) {
  return (
    <div className="flex items-center gap-3">
      <span className="text-4xl">🔥</span>
      <div>
        <div className="text-3xl font-bold text-gray-900">{streak}</div>
        <div className="text-sm text-gray-500 font-medium">day streak!</div>
      </div>
    </div>
  );
}
