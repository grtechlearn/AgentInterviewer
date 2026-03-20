"""
CoachAgent - Provides improvement tips after evaluation.
"""

from __future__ import annotations

import json
from typing import Any

from agentx.core.agent import BaseAgent, AgentConfig
from agentx.core.context import AgentContext
from agentx.core.message import AgentMessage

TIPS_BY_DOMAIN: dict[str, list[str]] = {
    "Python": [
        "Practice writing list comprehensions for cleaner code.",
        "Study decorators by building a caching decorator from scratch.",
        "Read the CPython source for deeper understanding of internals.",
        "Use type hints consistently for better code quality.",
    ],
    "JavaScript": [
        "Build a small project using only Promises, then convert to async/await.",
        "Study the V8 engine event loop in depth.",
        "Practice prototype-based patterns before using class syntax.",
        "Learn WeakMap and WeakSet for advanced memory management.",
    ],
    "React": [
        "Build a custom hook that manages form state.",
        "Profile your app using React DevTools to find re-render issues.",
        "Implement a component library with Storybook.",
        "Study React Fiber architecture for deeper understanding.",
    ],
    "SystemDesign": [
        "Practice drawing architecture diagrams on a whiteboard.",
        "Study real-world case studies from engineering blogs.",
        "Focus on trade-offs rather than perfect solutions.",
        "Learn to estimate capacity and make back-of-envelope calculations.",
    ],
}

RESOURCES: dict[str, list[str]] = {
    "Python": ["docs.python.org", "Real Python tutorials", "Python Cookbook by Beazley"],
    "JavaScript": ["MDN Web Docs", "javascript.info", "You Don't Know JS series"],
    "React": ["react.dev official docs", "Kent C. Dodds blog", "React patterns guide"],
    "SystemDesign": ["System Design Primer (GitHub)", "Designing Data-Intensive Applications", "ByteByteGo"],
}


class CoachAgent(BaseAgent):
    """Gives personalized improvement tips after an evaluation."""

    def __init__(self, **kwargs: Any):
        config = AgentConfig(
            name="coach",
            role="Interview Coach",
            system_prompt="You are a supportive interview coach helping candidates improve.",
        )
        super().__init__(config=config, **kwargs)

    async def process(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        evaluation = context.get("last_evaluation", message.data.get("evaluation", {}))
        domain = evaluation.get("domain", context.get("domain", "Python"))
        score = evaluation.get("score", 50)

        tips = TIPS_BY_DOMAIN.get(domain, TIPS_BY_DOMAIN["Python"])[:3]
        resources = RESOURCES.get(domain, RESOURCES["Python"])
        motivation = self._motivation(score)
        suggestion = self._next_topic(context)

        result = {
            "tips": tips,
            "resources": resources,
            "motivation_message": motivation,
            "next_topic_suggestion": suggestion,
            "domain": domain,
            "current_score": score,
        }
        return message.reply(content=json.dumps(result), data=result)

    def _motivation(self, score: int) -> str:
        if score >= 80:
            return "Outstanding work! You are interview-ready for this topic."
        if score >= 60:
            return "Great progress! A little more practice and you will ace it."
        if score >= 40:
            return "Good effort! Focus on the fundamentals and you will improve fast."
        return "Every expert was once a beginner. Keep practicing daily!"

    def _next_topic(self, context: AgentContext) -> str:
        covered = context.get("topics_covered", [])
        domain = context.get("domain", "Python")
        all_topics = {
            "Python": ["Data Structures", "Functions", "OOP", "Concurrency", "Memory", "Iterators"],
            "JavaScript": ["Async", "Variables", "OOP", "Functions", "Types", "DOM"],
            "React": ["Core", "Hooks", "State", "Performance", "SSR", "Testing"],
        }
        topics = all_topics.get(domain, ["Fundamentals", "Advanced Concepts", "Best Practices"])
        remaining = [t for t in topics if t not in covered]
        return remaining[0] if remaining else topics[0]
