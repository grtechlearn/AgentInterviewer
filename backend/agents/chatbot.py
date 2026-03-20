"""
ChatBotAgent - Free-form AI chat about tech topics.
"""

from __future__ import annotations

import json
from typing import Any

from agentx.core.agent import BaseAgent, AgentConfig
from agentx.core.context import AgentContext
from agentx.core.message import AgentMessage

CANNED_RESPONSES: dict[str, str] = {
    "python": "Python is a versatile, high-level programming language known for its readability. Key features include dynamic typing, garbage collection, and extensive standard library. It excels in web development, data science, AI/ML, and scripting.",
    "javascript": "JavaScript is the language of the web, running in browsers and on servers via Node.js. Key concepts include the event loop, closures, prototypal inheritance, and async programming with Promises and async/await.",
    "react": "React is a declarative UI library by Meta. It uses a virtual DOM for efficient rendering, components for reusability, and hooks for state management. Key patterns include lifting state up, render props, and custom hooks.",
    "interview": "For technical interviews, focus on: 1) Understanding fundamentals deeply, 2) Practicing problem-solving out loud, 3) Asking clarifying questions, 4) Discussing trade-offs, 5) Writing clean code with tests.",
    "system design": "System design interviews test your ability to design scalable systems. Key areas: load balancing, caching, database sharding, message queues, microservices, and CAP theorem. Always start with requirements gathering.",
    "data structures": "Essential data structures for interviews: arrays, linked lists, hash maps, trees (BST, heap), graphs, stacks, and queues. Know the time complexity of operations for each.",
    "algorithms": "Core algorithms to master: sorting (merge, quick, heap), searching (binary search, BFS, DFS), dynamic programming, greedy algorithms, and two-pointer technique.",
    "career": "To grow your career in tech: 1) Build projects, 2) Contribute to open source, 3) Network on LinkedIn, 4) Practice interviews regularly, 5) Stay current with industry trends.",
    "resume": "A strong tech resume includes: clear contact info, a skills section with technologies, work experience with quantified achievements, relevant projects, and education. Keep it to 1-2 pages.",
    "salary": "Research market rates on levels.fyi and Glassdoor. In negotiations, focus on total compensation including stock, bonuses, and benefits. Always negotiate your first offer.",
}

DEFAULT_RESPONSE = (
    "That is a great question! While I am in mock mode and have limited "
    "responses, I can help you practice interview questions across Python, "
    "JavaScript, React, System Design, and more. Try asking about a specific "
    "technology or interview topic!"
)


class ChatBotAgent(BaseAgent):
    """Free-form chat about tech and interview topics."""

    def __init__(self, **kwargs: Any):
        config = AgentConfig(
            name="chatbot",
            role="Tech Chat Assistant",
            system_prompt=(
                "You are a friendly tech mentor who helps candidates prepare "
                "for interviews. Answer questions about programming, system "
                "design, career advice, and interview tips."
            ),
        )
        super().__init__(config=config, **kwargs)

    async def process(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        query = message.content.lower().strip()

        # Find best matching canned response
        best_match = DEFAULT_RESPONSE
        best_score = 0
        for key, response in CANNED_RESPONSES.items():
            words = key.split()
            score = sum(1 for w in words if w in query)
            if score > best_score:
                best_score = score
                best_match = response

        result = {
            "response": best_match,
            "mock_mode": True,
            "suggestion": "Try asking about a specific topic like Python, React, or System Design.",
        }
        return message.reply(content=json.dumps(result), data=result)
