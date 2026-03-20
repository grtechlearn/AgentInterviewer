"""
MotivatorAgent - Daily motivation and topic of the day.
"""

from __future__ import annotations

import json
import random
from datetime import datetime, timezone
from typing import Any

from agentx.core.agent import BaseAgent, AgentConfig
from agentx.core.context import AgentContext
from agentx.core.message import AgentMessage

DAILY_MESSAGES = [
    "Consistency beats intensity. One question a day keeps rejection away!",
    "Every interview you practice makes the real one easier.",
    "You are one commit closer to your dream job.",
    "The best developers never stop learning. Neither should you.",
    "Mistakes in practice are lessons. Mistakes in interviews are stories.",
    "Your future self will thank you for practicing today.",
    "Focus on understanding, not memorization. Interviewers can tell the difference.",
    "Great developers are made, not born. Keep building your skills.",
    "Today is a great day to master something new.",
    "Remember: every expert was once a beginner who did not quit.",
]

TOPICS_OF_DAY = [
    {"topic": "Closures in JavaScript", "domain": "JavaScript", "why": "Frequently asked in frontend interviews."},
    {"topic": "Database Indexing", "domain": "SystemDesign", "why": "Critical for system design rounds."},
    {"topic": "Python Generators", "domain": "Python", "why": "Shows advanced Python knowledge."},
    {"topic": "React useEffect cleanup", "domain": "React", "why": "Common source of bugs in real apps."},
    {"topic": "REST vs GraphQL", "domain": "SystemDesign", "why": "Modern API design is a hot topic."},
    {"topic": "Git branching strategies", "domain": "DevOps", "why": "Shows team collaboration skills."},
    {"topic": "SOLID Principles", "domain": "Java", "why": "Foundation of good OOP design."},
]

MILESTONES = {
    10: "First 10 questions completed! You are building momentum.",
    25: "25 questions done! You are in the top 20% of users.",
    50: "Half century! 50 questions shows real dedication.",
    100: "100 questions! You are a practice machine.",
    7: "7-day streak! Consistency is your superpower.",
    30: "30-day streak! You are unstoppable.",
}


class MotivatorAgent(BaseAgent):
    """Delivers motivation, daily topics, and milestone celebrations."""

    def __init__(self, **kwargs: Any):
        config = AgentConfig(
            name="motivator",
            role="Motivation Coach",
            system_prompt="You inspire and motivate candidates to keep practicing.",
        )
        super().__init__(config=config, **kwargs)

    async def process(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        action = message.data.get("action", "daily_message")

        if action == "daily_message":
            return self._daily_message(message, context)
        if action == "topic_of_day":
            return self._topic_of_day(message, context)
        if action == "celebrate_milestone":
            return self._celebrate(message, context)

        return message.error(f"Unknown motivator action: {action}")

    def _daily_message(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        day_index = datetime.now(timezone.utc).timetuple().tm_yday
        msg = DAILY_MESSAGES[day_index % len(DAILY_MESSAGES)]
        streak = context.get("streak", 0)

        result = {
            "message": msg,
            "streak": streak,
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        }
        return message.reply(content=json.dumps(result), data=result)

    def _topic_of_day(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        day_index = datetime.now(timezone.utc).timetuple().tm_yday
        topic = TOPICS_OF_DAY[day_index % len(TOPICS_OF_DAY)]
        result = {
            "topic_of_day": topic["topic"],
            "domain": topic["domain"],
            "why": topic["why"],
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        }
        return message.reply(content=json.dumps(result), data=result)

    def _celebrate(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        total_questions = len(context.get("evaluations", []))
        streak = context.get("streak", 0)

        celebrations = []
        for threshold, msg in MILESTONES.items():
            if total_questions == threshold or streak == threshold:
                celebrations.append(msg)

        if not celebrations:
            celebrations.append(f"Keep going! {total_questions} questions completed so far.")

        result = {
            "celebrations": celebrations,
            "total_questions": total_questions,
            "streak": streak,
        }
        return message.reply(content=json.dumps(result), data=result)
