"""
ReportAgent - Generates a session summary report.
"""

from __future__ import annotations

import json
from typing import Any

from agentx.core.agent import BaseAgent, AgentConfig
from agentx.core.context import AgentContext
from agentx.core.message import AgentMessage

STUDY_PLANS: dict[str, list[str]] = {
    "Python": ["Complete Python Data Structures module", "Practice 5 decorator problems", "Build a project using asyncio"],
    "JavaScript": ["Master Promises and async/await", "Build a closure-based module pattern", "Study event loop internals"],
    "React": ["Build 3 custom hooks", "Optimize a slow component with profiling", "Implement SSR with Next.js"],
    "SystemDesign": ["Design 2 systems per week", "Practice capacity estimation", "Read 3 engineering blogs"],
}


class ReportAgent(BaseAgent):
    """Generates end-of-session reports with strengths, weaknesses, and study plan."""

    def __init__(self, **kwargs: Any):
        config = AgentConfig(
            name="report",
            role="Session Report Generator",
            system_prompt="You produce clear, actionable interview session reports.",
        )
        super().__init__(config=config, **kwargs)

    async def process(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        evaluations = context.get("evaluations", [])
        domain = context.get("domain", "Python")

        if not evaluations:
            result = {"overall_score": 0, "message": "No evaluations found for this session."}
            return message.reply(content=json.dumps(result), data=result)

        scores = [e.get("score", 0) for e in evaluations]
        overall = round(sum(scores) / len(scores), 1)

        breakdown = []
        strengths = []
        weaknesses = []
        for i, ev in enumerate(evaluations, 1):
            breakdown.append({
                "question_number": i,
                "question": ev.get("question", ""),
                "score": ev.get("score", 0),
                "topic": ev.get("domain", domain),
            })
            for pt in ev.get("correct_points", []):
                if pt not in strengths:
                    strengths.append(pt)
            for pt in ev.get("missing_points", []):
                if pt not in weaknesses:
                    weaknesses.append(pt)

        plan = STUDY_PLANS.get(domain, STUDY_PLANS["Python"])
        next_rec = self._recommend_next(overall, domain)

        result = {
            "overall_score": overall,
            "total_questions": len(evaluations),
            "per_question_breakdown": breakdown,
            "strengths": strengths[:5],
            "weaknesses": weaknesses[:5],
            "study_plan": plan,
            "next_recommended": next_rec,
            "domain": domain,
        }
        return message.reply(content=json.dumps(result), data=result)

    def _recommend_next(self, score: float, domain: str) -> str:
        if score >= 80:
            return f"Try advanced {domain} questions or move to System Design."
        if score >= 50:
            return f"Continue with {domain} at a higher difficulty."
        return f"Review {domain} fundamentals before attempting more questions."
