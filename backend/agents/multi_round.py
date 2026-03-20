"""
MultiRoundAgent - Manages a multi-round interview pipeline.
"""

from __future__ import annotations

import json
from typing import Any

from agentx.core.agent import BaseAgent, AgentConfig
from agentx.core.context import AgentContext
from agentx.core.message import AgentMessage

ROUNDS: list[dict[str, Any]] = [
    {"name": "phone_screen", "difficulty": "easy", "questions": 5,
     "description": "Initial screening to assess basic knowledge."},
    {"name": "technical", "difficulty": "medium", "questions": 8,
     "description": "Deep-dive into technical skills and problem solving."},
    {"name": "system_design", "difficulty": "hard", "questions": 2,
     "description": "Evaluate architecture and design thinking."},
    {"name": "behavioral", "difficulty": "medium", "questions": 5,
     "description": "Assess culture fit and soft skills."},
    {"name": "offer", "difficulty": "medium", "questions": 3,
     "description": "Salary negotiation and offer discussion."},
]

TOTAL_ROUNDS = len(ROUNDS)


class MultiRoundAgent(BaseAgent):
    """Manages a full multi-round interview pipeline."""

    def __init__(self, **kwargs: Any):
        config = AgentConfig(
            name="multi_round",
            role="Multi-Round Interview Pipeline Manager",
            system_prompt=(
                "You manage a five-round interview pipeline: phone screen, "
                "technical, system design, behavioral, and offer negotiation. "
                "Track progress and scores across all rounds."
            ),
        )
        super().__init__(config=config, **kwargs)

    async def process(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        action = message.data.get("action", "start_pipeline")

        if action == "start_pipeline":
            return self._start_pipeline(message, context)
        if action == "next_round":
            return self._next_round(message, context)
        if action == "get_pipeline_status":
            return self._get_status(message, context)
        if action == "pipeline_report":
            return self._pipeline_report(message, context)

        return message.error(f"Unknown action: {action}")

    # ------------------------------------------------------------------

    def _start_pipeline(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        context.set("pipeline_round", 0)
        context.set("pipeline_scores", {})
        context.set("pipeline_started", True)

        current = ROUNDS[0]
        result = {
            "status": "pipeline_started",
            "current_round": 0,
            "round_name": current["name"],
            "difficulty": current["difficulty"],
            "questions_in_round": current["questions"],
            "description": current["description"],
            "total_rounds": TOTAL_ROUNDS,
            "overall_progress": 0,
        }
        return message.reply(content=json.dumps(result), data=result)

    def _next_round(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        current_idx = context.get("pipeline_round", 0)
        round_score = message.data.get("round_score", 0)

        # Store score for completed round
        scores = context.get("pipeline_scores", {})
        scores[ROUNDS[current_idx]["name"]] = round_score
        context.set("pipeline_scores", scores)

        next_idx = current_idx + 1
        if next_idx >= TOTAL_ROUNDS:
            context.set("pipeline_round", current_idx)
            result = {
                "status": "pipeline_complete",
                "message": "All rounds completed.",
                "overall_progress": 100,
                "scores": scores,
            }
            return message.reply(content=json.dumps(result), data=result)

        context.set("pipeline_round", next_idx)
        current = ROUNDS[next_idx]
        progress = int((next_idx / TOTAL_ROUNDS) * 100)

        result = {
            "status": "round_started",
            "current_round": next_idx,
            "round_name": current["name"],
            "difficulty": current["difficulty"],
            "questions_in_round": current["questions"],
            "description": current["description"],
            "total_rounds": TOTAL_ROUNDS,
            "overall_progress": progress,
        }
        return message.reply(content=json.dumps(result), data=result)

    def _get_status(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        current_idx = context.get("pipeline_round", 0)
        scores = context.get("pipeline_scores", {})
        started = context.get("pipeline_started", False)

        if not started:
            result = {"status": "not_started", "overall_progress": 0}
            return message.reply(content=json.dumps(result), data=result)

        current = ROUNDS[current_idx]
        progress = int((current_idx / TOTAL_ROUNDS) * 100)

        result = {
            "status": "in_progress",
            "current_round": current_idx,
            "round_name": current["name"],
            "difficulty": current["difficulty"],
            "questions_in_round": current["questions"],
            "overall_progress": progress,
            "completed_rounds": list(scores.keys()),
            "scores": scores,
        }
        return message.reply(content=json.dumps(result), data=result)

    def _pipeline_report(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        scores = context.get("pipeline_scores", {})
        total = sum(scores.values()) if scores else 0
        count = len(scores) if scores else 1
        average = total // count if count else 0

        round_details = []
        for r in ROUNDS:
            score = scores.get(r["name"])
            round_details.append({
                "round_name": r["name"],
                "difficulty": r["difficulty"],
                "questions": r["questions"],
                "score": score,
                "completed": score is not None,
            })

        result = {
            "status": "report",
            "total_score": total,
            "average_score": average,
            "rounds_completed": len(scores),
            "total_rounds": TOTAL_ROUNDS,
            "round_details": round_details,
            "recommendation": self._recommendation(average, len(scores)),
        }
        return message.reply(content=json.dumps(result), data=result)

    @staticmethod
    def _recommendation(avg: int, completed: int) -> str:
        if completed < TOTAL_ROUNDS:
            return "Pipeline incomplete. Complete all rounds for a full assessment."
        if avg >= 80:
            return "Strong candidate. Recommend proceeding to offer."
        if avg >= 60:
            return "Promising candidate. Consider additional assessment."
        return "Below threshold. Recommend further preparation."
