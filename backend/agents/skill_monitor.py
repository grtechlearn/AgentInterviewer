"""
SkillMonitorAgent - Tracks skill levels per domain.
"""

from __future__ import annotations

import json
from typing import Any

from agentx.core.agent import BaseAgent, AgentConfig
from agentx.core.context import AgentContext
from agentx.core.message import AgentMessage

LEVEL_BANDS = [
    (0, 30, "beginner"),
    (31, 70, "intermediate"),
    (71, 100, "advanced"),
]


def _skill_level(score: int) -> str:
    for lo, hi, label in LEVEL_BANDS:
        if lo <= score <= hi:
            return label
    return "beginner"


class SkillMonitorAgent(BaseAgent):
    """Maintains and reports skill levels across domains."""

    def __init__(self, **kwargs: Any):
        config = AgentConfig(
            name="skill_monitor",
            role="Skill Level Tracker",
            system_prompt="You track and report candidate skill levels across domains.",
        )
        super().__init__(config=config, **kwargs)

    async def process(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        action = message.data.get("action", "get_skills")

        if action == "update_skill":
            return self._update_skill(message, context)
        if action == "get_skills":
            return self._get_skills(message, context)
        if action == "get_weak_areas":
            return self._get_weak_areas(message, context)

        return message.error(f"Unknown skill_monitor action: {action}")

    def _update_skill(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        domain = message.data.get("domain", "Python")
        score = message.data.get("score", 50)

        skills: dict[str, dict[str, Any]] = context.get("skills", {})
        existing = skills.get(domain, {"score": 0, "attempts": 0, "history": []})

        attempts = existing["attempts"] + 1
        # Weighted average: recent scores matter more
        old_score = existing["score"]
        new_score = round((old_score * 0.6) + (score * 0.4)) if old_score > 0 else score
        new_score = max(0, min(100, new_score))

        history = existing.get("history", [])
        history.append(score)
        if len(history) > 20:
            history = history[-20:]

        skills[domain] = {
            "score": new_score,
            "level": _skill_level(new_score),
            "attempts": attempts,
            "history": history,
        }
        context.set("skills", skills)

        result = {
            "domain": domain,
            "score": new_score,
            "level": _skill_level(new_score),
            "attempts": attempts,
            "previous_score": old_score,
            "change": new_score - old_score,
        }
        return message.reply(content=json.dumps(result), data=result)

    def _get_skills(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        skills = context.get("skills", {})
        summary = []
        for domain, info in skills.items():
            summary.append({
                "domain": domain,
                "score": info["score"],
                "level": info["level"],
                "attempts": info["attempts"],
            })

        result = {"skills": summary, "total_domains": len(summary)}
        return message.reply(content=json.dumps(result), data=result)

    def _get_weak_areas(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        skills = context.get("skills", {})
        weak = [
            {"domain": d, "score": info["score"], "level": info["level"]}
            for d, info in skills.items()
            if info["score"] < 50
        ]
        weak.sort(key=lambda x: x["score"])

        result = {
            "weak_areas": weak,
            "recommendation": "Focus on your weakest domain first." if weak else "No weak areas detected. Great work!",
        }
        return message.reply(content=json.dumps(result), data=result)
