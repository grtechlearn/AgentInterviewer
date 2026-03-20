"""
GoalTrackerAgent - Manages user goals and streaks.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from agentx.core.agent import BaseAgent, AgentConfig
from agentx.core.context import AgentContext
from agentx.core.message import AgentMessage


class GoalTrackerAgent(BaseAgent):
    """Tracks daily goals, weekly targets, and streaks."""

    def __init__(self, **kwargs: Any):
        config = AgentConfig(
            name="goal_tracker",
            role="Goal & Streak Tracker",
            system_prompt="You help users set and track their interview preparation goals.",
        )
        super().__init__(config=config, **kwargs)

    async def process(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        action = message.data.get("action", "get_progress")

        if action == "set_goal":
            return self._set_goal(message, context)
        if action == "get_progress":
            return self._get_progress(message, context)
        if action == "update_streak":
            return self._update_streak(message, context)
        if action == "check_daily":
            return self._check_daily(message, context)

        return message.error(f"Unknown goal_tracker action: {action}")

    def _set_goal(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        goal = {
            "domain": message.data.get("domain", "Python"),
            "daily_questions": message.data.get("daily_questions", 5),
            "weekly_target": message.data.get("weekly_target", 25),
            "target_score": message.data.get("target_score", 70),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        goals = context.get("goals", [])
        goals.append(goal)
        context.set("goals", goals)

        result = {"status": "goal_set", "goal": goal}
        return message.reply(content=json.dumps(result), data=result)

    def _get_progress(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        goals = context.get("goals", [])
        evaluations = context.get("evaluations", [])
        streak = context.get("streak", 0)

        completed = len(evaluations)
        avg_score = 0.0
        if evaluations:
            avg_score = sum(e.get("score", 0) for e in evaluations) / len(evaluations)

        current_goal = goals[-1] if goals else {"daily_questions": 5, "target_score": 70}
        daily_target = current_goal.get("daily_questions", 5)
        daily_progress = min(100, int((completed / max(1, daily_target)) * 100))

        result = {
            "questions_completed": completed,
            "average_score": round(avg_score, 1),
            "current_streak": streak,
            "daily_progress_pct": daily_progress,
            "daily_target": daily_target,
            "target_score": current_goal.get("target_score", 70),
            "on_track": avg_score >= current_goal.get("target_score", 70),
        }
        return message.reply(content=json.dumps(result), data=result)

    def _update_streak(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        streak = context.get("streak", 0) + 1
        context.set("streak", streak)
        best = context.get("best_streak", 0)
        if streak > best:
            context.set("best_streak", streak)
            best = streak

        result = {"current_streak": streak, "best_streak": best, "streak_updated": True}
        return message.reply(content=json.dumps(result), data=result)

    def _check_daily(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        evaluations = context.get("evaluations", [])
        goals = context.get("goals", [])
        daily_target = 5
        if goals:
            daily_target = goals[-1].get("daily_questions", 5)

        done = len(evaluations)
        remaining = max(0, daily_target - done)
        result = {
            "daily_target": daily_target,
            "completed_today": done,
            "remaining": remaining,
            "daily_complete": remaining == 0,
            "message": "Great job, daily goal met!" if remaining == 0 else f"{remaining} more questions to go!",
        }
        return message.reply(content=json.dumps(result), data=result)
