"""
PanelInterviewerAgent - Simulates a panel interview with multiple personas.
"""

from __future__ import annotations

import json
import random
from typing import Any

from agentx.core.agent import BaseAgent, AgentConfig
from agentx.core.context import AgentContext
from agentx.core.message import AgentMessage

PERSONAS: list[dict[str, Any]] = [
    {
        "name": "Priya Sharma",
        "role": "Technical Lead",
        "focus": "deep_technical",
        "style": "Thorough and detail-oriented",
        "questions": [
            "Walk me through how you would debug a memory leak in production.",
            "Explain the trade-offs between SQL and NoSQL for this use case.",
            "How would you implement a thread-safe singleton in your language?",
            "Describe your approach to writing unit tests for async code.",
            "What design patterns have you applied in a real project?",
        ],
    },
    {
        "name": "Arjun Mehta",
        "role": "System Architect",
        "focus": "breadth_and_design",
        "style": "Big-picture thinker who probes scalability",
        "questions": [
            "Design a notification system that handles 10M users.",
            "How would you migrate a monolith to microservices?",
            "Explain your approach to API versioning at scale.",
            "What caching strategy would you use for a social feed?",
            "How do you ensure data consistency across distributed services?",
        ],
    },
    {
        "name": "Kavitha Rajan",
        "role": "HR Manager",
        "focus": "behavioral",
        "style": "Empathetic listener focused on culture fit",
        "questions": [
            "Tell me about a time you disagreed with your manager.",
            "How do you prioritize when everything feels urgent?",
            "Describe a situation where you had to learn something quickly.",
            "What motivates you to do your best work?",
            "How do you give constructive feedback to a peer?",
        ],
    },
]


class PanelInterviewerAgent(BaseAgent):
    """Simulates a panel interview rotating between three personas."""

    def __init__(self, **kwargs: Any):
        config = AgentConfig(
            name="panel_interviewer",
            role="Panel Interview Simulator",
            system_prompt=(
                "You simulate a panel interview with three interviewers: "
                "a Technical Lead, a System Architect, and an HR Manager. "
                "Each asks questions from their area of expertise."
            ),
        )
        super().__init__(config=config, **kwargs)

    async def process(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        action = message.data.get("action", "start_panel")

        if action == "start_panel":
            return self._start_panel(message, context)
        if action == "panel_question":
            return self._panel_question(message, context)
        if action == "panel_evaluate":
            return self._panel_evaluate(message, context)

        return message.error(f"Unknown action: {action}")

    # ------------------------------------------------------------------

    def _start_panel(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        context.set("panel_index", 0)
        context.set("panel_question_num", 0)
        context.set("panel_scores", [])

        panel_info = [
            {"name": p["name"], "role": p["role"], "focus": p["focus"]}
            for p in PERSONAS
        ]
        result = {
            "status": "panel_started",
            "panel": panel_info,
            "total_personas": len(PERSONAS),
            "message": "Panel interview initiated. Three interviewers are ready.",
        }
        return message.reply(content=json.dumps(result), data=result)

    def _panel_question(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        q_num = context.get("panel_question_num", 0)
        persona_idx = q_num % len(PERSONAS)
        persona = PERSONAS[persona_idx]

        q_idx = (q_num // len(PERSONAS)) % len(persona["questions"])
        question_text = persona["questions"][q_idx]

        context.set("panel_question_num", q_num + 1)
        context.set("panel_index", persona_idx)

        result = {
            "question": question_text,
            "persona_name": persona["name"],
            "persona_role": persona["role"],
            "focus_area": persona["focus"],
            "question_number": q_num + 1,
            "style": persona["style"],
        }
        return message.reply(content=json.dumps(result), data=result)

    def _panel_evaluate(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        answer = message.data.get("answer", "")
        persona_idx = context.get("panel_index", 0)
        persona = PERSONAS[persona_idx]

        # Mock scoring based on answer length
        length_score = min(50, len(answer) // 5)
        base_score = min(100, length_score + random.randint(30, 60))

        scores = context.get("panel_scores", [])
        entry = {
            "persona_name": persona["name"],
            "persona_role": persona["role"],
            "score": base_score,
            "feedback": self._mock_feedback(base_score, persona["role"]),
        }
        scores.append(entry)
        context.set("panel_scores", scores)

        result = {
            **entry,
            "total_evaluations": len(scores),
            "average_score": sum(s["score"] for s in scores) // len(scores),
        }
        return message.reply(content=json.dumps(result), data=result)

    @staticmethod
    def _mock_feedback(score: int, role: str) -> str:
        if score >= 80:
            return f"[{role}] Excellent response with strong depth."
        if score >= 60:
            return f"[{role}] Good answer. Could add more specifics."
        return f"[{role}] Needs improvement. Review core concepts."
