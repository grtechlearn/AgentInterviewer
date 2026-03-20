"""
EvaluatorAgent - Scores candidate answers.
"""

from __future__ import annotations

import json
from typing import Any

from agentx.core.agent import BaseAgent, AgentConfig
from agentx.core.context import AgentContext
from agentx.core.message import AgentMessage

# Keywords per domain used for mock scoring
DOMAIN_KEYWORDS: dict[str, list[str]] = {
    "Python": ["class", "def", "lambda", "generator", "decorator", "GIL", "async", "list", "dict", "tuple", "yield", "comprehension", "import", "module"],
    "JavaScript": ["closure", "prototype", "promise", "async", "await", "callback", "scope", "hoisting", "event loop", "this", "arrow", "const", "let"],
    "React": ["component", "hook", "state", "props", "render", "virtual DOM", "useEffect", "useState", "context", "redux", "memo", "ref"],
    "iOS": ["swift", "ARC", "struct", "class", "protocol", "delegate", "SwiftUI", "UIKit", "optional", "guard", "enum"],
    "Android": ["activity", "fragment", "compose", "viewmodel", "coroutine", "intent", "broadcast", "service", "room", "hilt"],
    "ReactNative": ["bridge", "native module", "FlatList", "navigation", "expo", "metro", "JSI", "fabric", "turbo"],
    "Java": ["JVM", "garbage", "stream", "thread", "interface", "abstract", "spring", "bean", "annotation", "generic"],
    "DevOps": ["docker", "kubernetes", "CI/CD", "pipeline", "terraform", "monitoring", "deploy", "container", "helm", "ansible"],
    "SystemDesign": ["scale", "shard", "cache", "load balancer", "queue", "microservice", "database", "API", "latency", "throughput"],
    "HR": ["team", "project", "challenge", "leadership", "communication", "conflict", "goal", "growth", "feedback", "collaboration"],
}


class EvaluatorAgent(BaseAgent):
    """Scores interview answers using keyword matching in mock mode."""

    def __init__(self, **kwargs: Any):
        config = AgentConfig(
            name="evaluator",
            role="Answer Evaluator",
            system_prompt=(
                "You are a fair technical evaluator. Score the answer on "
                "correctness, completeness, and clarity."
            ),
        )
        super().__init__(config=config, **kwargs)

    async def process(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        question = message.data.get("question", "")
        answer = message.data.get("answer", "")
        domain = message.data.get("domain", context.get("domain", "Python"))

        score, correct, incorrect, missing = self._mock_evaluate(
            answer, domain
        )

        difficulty = context.get("difficulty", "medium")
        adjustment = "same"
        if score >= 80:
            adjustment = "harder"
        elif score <= 40:
            adjustment = "easier"

        xp = max(5, int(score * 0.5))

        result = {
            "score": score,
            "correct_points": correct,
            "incorrect_points": incorrect,
            "missing_points": missing,
            "explanation": self._build_explanation(score),
            "difficulty_adjustment": adjustment,
            "xp_earned": xp,
            "question": question,
            "domain": domain,
        }

        # Store for downstream agents
        evals = context.get("evaluations", [])
        evals.append(result)
        context.set("evaluations", evals)
        context.set("last_evaluation", result)

        return message.reply(content=json.dumps(result), data=result)

    # ------------------------------------------------------------------

    def _mock_evaluate(
        self, answer: str, domain: str
    ) -> tuple[int, list[str], list[str], list[str]]:
        keywords = DOMAIN_KEYWORDS.get(domain, DOMAIN_KEYWORDS["Python"])
        answer_lower = answer.lower()

        matched = [kw for kw in keywords if kw.lower() in answer_lower]
        missed = [kw for kw in keywords if kw.lower() not in answer_lower]

        # Length bonus
        length_score = min(30, len(answer) // 10)
        keyword_score = min(50, len(matched) * 10)
        base_score = min(100, length_score + keyword_score + 20)

        correct = [f"Mentioned {kw}" for kw in matched[:5]]
        incorrect = []
        if len(answer) < 20:
            incorrect.append("Answer is too brief")
            base_score = max(10, base_score - 20)
        missing = [f"Could mention {kw}" for kw in missed[:3]]

        return base_score, correct, incorrect, missing

    def _build_explanation(self, score: int) -> str:
        if score >= 80:
            return "Excellent answer demonstrating strong understanding."
        if score >= 60:
            return "Good answer with room for more depth."
        if score >= 40:
            return "Partial answer. Review the fundamentals."
        return "Needs significant improvement. Study this topic thoroughly."
