"""
SalaryCoachAgent - Salary negotiation practice and coaching.
"""

from __future__ import annotations

import json
import random
from typing import Any

from agentx.core.agent import BaseAgent, AgentConfig
from agentx.core.context import AgentContext
from agentx.core.message import AgentMessage

MOCK_OFFERS: list[dict[str, Any]] = [
    {"role": "Software Engineer", "company": "TechCorp", "base": 1200000, "currency": "INR"},
    {"role": "Frontend Developer", "company": "WebScale", "base": 900000, "currency": "INR"},
    {"role": "Backend Engineer", "company": "CloudNine", "base": 1500000, "currency": "INR"},
    {"role": "Full Stack Developer", "company": "StartupX", "base": 1000000, "currency": "INR"},
    {"role": "Data Engineer", "company": "DataFlow", "base": 1400000, "currency": "INR"},
]

NEGOTIATION_TIPS: list[str] = [
    "Always research the market rate before negotiating.",
    "Never reveal your current salary first.",
    "Focus on total compensation, not just base salary.",
    "Express enthusiasm for the role before negotiating.",
    "Use data from levels.fyi and Glassdoor to back your ask.",
    "Consider stock options, bonuses, and benefits in your evaluation.",
    "Practice the conversation out loud before the real call.",
    "Have a walk-away number decided in advance.",
    "Negotiate over email if you are uncomfortable on the phone.",
    "Silence is a powerful tool — let the recruiter fill gaps.",
]

STRATEGY_EVALUATIONS: dict[str, dict[str, Any]] = {
    "aggressive": {"rating": 5, "feedback": "Too aggressive. You risk losing the offer entirely. Soften your approach."},
    "confident": {"rating": 9, "feedback": "Great approach. You backed your ask with data and stayed professional."},
    "passive": {"rating": 4, "feedback": "Too passive. You accepted without exploring room for improvement."},
    "reasonable": {"rating": 8, "feedback": "Good balance. You negotiated firmly but fairly."},
    "default": {"rating": 6, "feedback": "Decent attempt. Try to quantify your value with specific achievements."},
}


class SalaryCoachAgent(BaseAgent):
    """Salary negotiation practice and coaching."""

    def __init__(self, **kwargs: Any):
        config = AgentConfig(
            name="salary_coach",
            role="Salary Negotiation Coach",
            system_prompt=(
                "You are an expert salary negotiation coach. Help candidates "
                "practice negotiations and provide actionable feedback."
            ),
        )
        super().__init__(config=config, **kwargs)

    async def process(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        action = message.data.get("action", "start_negotiation")

        if action == "start_negotiation":
            return self._start_negotiation(message, context)
        if action == "respond":
            return self._respond(message, context)
        if action == "get_tips":
            return self._get_tips(message, context)

        return message.error(f"Unknown action: {action}")

    def _start_negotiation(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        offer = random.choice(MOCK_OFFERS)
        context.set("current_offer", offer)
        context.set("negotiation_round", 1)
        result = {
            "offer_amount": offer["base"],
            "role": offer["role"],
            "company": offer["company"],
            "currency": offer["currency"],
            "message": f"Congratulations! {offer['company']} is offering you the {offer['role']} position at {offer['currency']} {offer['base']:,}/year. How would you like to respond?",
            "mock_mode": True,
        }
        return message.reply(content=json.dumps(result), data=result)

    def _respond(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        user_response = message.data.get("response", "").lower()
        offer = context.get("current_offer", MOCK_OFFERS[0])
        round_num = context.get("negotiation_round", 1)

        # Classify strategy
        strategy = "default"
        if any(w in user_response for w in ("demand", "must", "minimum", "or else")):
            strategy = "aggressive"
        elif any(w in user_response for w in ("research", "market", "data", "value")):
            strategy = "confident"
        elif any(w in user_response for w in ("accept", "fine", "okay", "sure")):
            strategy = "passive"
        elif any(w in user_response for w in ("consider", "fair", "flexible", "discuss")):
            strategy = "reasonable"

        evaluation = STRATEGY_EVALUATIONS[strategy]
        bump = int(offer["base"] * 0.1) if strategy in ("confident", "reasonable") else 0
        counter = offer["base"] + bump

        context.set("negotiation_round", round_num + 1)

        result = {
            "evaluation": evaluation["feedback"],
            "rating": evaluation["rating"],
            "strategy_detected": strategy,
            "counter_offer_suggestion": counter,
            "round": round_num,
            "tips": random.sample(NEGOTIATION_TIPS, min(3, len(NEGOTIATION_TIPS))),
            "mock_mode": True,
        }
        return message.reply(content=json.dumps(result), data=result)

    def _get_tips(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        count = message.data.get("count", 5)
        tips = random.sample(NEGOTIATION_TIPS, min(count, len(NEGOTIATION_TIPS)))
        result = {"tips": tips, "total_available": len(NEGOTIATION_TIPS), "mock_mode": True}
        return message.reply(content=json.dumps(result), data=result)
