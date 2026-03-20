"""
AdminAnalyticsAgent - Generate admin dashboard reports and analytics.
"""

from __future__ import annotations

import json
import random
from typing import Any

from agentx.core.agent import BaseAgent, AgentConfig
from agentx.core.context import AgentContext
from agentx.core.message import AgentMessage

MOCK_DOMAINS = ["Python", "JavaScript", "React", "Java", "SystemDesign", "DevOps", "iOS", "Android"]


class AdminAnalyticsAgent(BaseAgent):
    """Generate admin reports with mock analytics data."""

    def __init__(self, **kwargs: Any):
        config = AgentConfig(
            name="admin_analytics",
            role="Admin Analytics Reporter",
            system_prompt=(
                "You generate admin dashboard analytics including user stats, "
                "agent performance, and cost reports."
            ),
        )
        super().__init__(config=config, **kwargs)

    async def process(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        action = message.data.get("action", "system_overview")

        if action == "system_overview":
            return self._system_overview(message, context)
        if action == "user_report":
            return self._user_report(message, context)
        if action == "agent_performance":
            return self._agent_performance(message, context)
        if action == "cost_report":
            return self._cost_report(message, context)

        return message.error(f"Unknown action: {action}")

    def _system_overview(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        result = {
            "total_users": 1247,
            "active_users": 389,
            "interviews_today": 156,
            "interviews_this_week": 892,
            "top_domains": random.sample(MOCK_DOMAINS, 3),
            "avg_session_duration_min": 18.5,
            "system_uptime_pct": 99.7,
            "mock_mode": True,
        }
        return message.reply(content=json.dumps(result), data=result)

    def _user_report(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        period = message.data.get("period", "weekly")
        result = {
            "period": period,
            "new_signups": 87,
            "returning_users": 302,
            "churned_users": 15,
            "retention_rate_pct": 82.3,
            "top_user_domains": [
                {"domain": "Python", "users": 145},
                {"domain": "JavaScript", "users": 98},
                {"domain": "React", "users": 76},
            ],
            "avg_interviews_per_user": 3.2,
            "mock_mode": True,
        }
        return message.reply(content=json.dumps(result), data=result)

    def _agent_performance(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        agents = [
            {"agent": "interviewer", "requests": 420, "avg_latency_ms": 145, "error_rate_pct": 0.5},
            {"agent": "evaluator", "requests": 380, "avg_latency_ms": 210, "error_rate_pct": 0.8},
            {"agent": "coach", "requests": 195, "avg_latency_ms": 180, "error_rate_pct": 0.3},
            {"agent": "chatbot", "requests": 310, "avg_latency_ms": 95, "error_rate_pct": 0.1},
            {"agent": "quiz_master", "requests": 150, "avg_latency_ms": 120, "error_rate_pct": 0.2},
            {"agent": "salary_coach", "requests": 45, "avg_latency_ms": 130, "error_rate_pct": 0.0},
        ]
        result = {
            "agents": agents,
            "total_requests": sum(a["requests"] for a in agents),
            "overall_error_rate_pct": 0.4,
            "mock_mode": True,
        }
        return message.reply(content=json.dumps(result), data=result)

    def _cost_report(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        period = message.data.get("period", "monthly")
        result = {
            "period": period,
            "total_cost_usd": 284.50,
            "cost_breakdown": [
                {"category": "LLM API calls", "cost_usd": 195.00, "pct": 68.5},
                {"category": "Infrastructure", "cost_usd": 55.00, "pct": 19.3},
                {"category": "Storage", "cost_usd": 18.50, "pct": 6.5},
                {"category": "Bandwidth", "cost_usd": 16.00, "pct": 5.6},
            ],
            "cost_per_interview_usd": 0.32,
            "projected_monthly_usd": 310.00,
            "mock_mode": True,
        }
        return message.reply(content=json.dumps(result), data=result)
