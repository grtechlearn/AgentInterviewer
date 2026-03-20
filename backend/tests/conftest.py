"""
Shared fixtures for AgentInterviewer test suite.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest

# Ensure agentx is importable
AGENTX_ROOT = Path(__file__).resolve().parents[3] / "agentx"
if str(AGENTX_ROOT) not in sys.path:
    sys.path.insert(0, str(AGENTX_ROOT))

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT.parent) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT.parent))

from agentx.core.context import AgentContext
from agentx.core.message import AgentMessage, MessageType


@pytest.fixture
def create_message():
    """Factory fixture to create AgentMessage instances."""

    def _create(
        content: str = "",
        data: dict[str, Any] | None = None,
        sender: str = "user",
        receiver: str = "agent",
        msg_type: MessageType = MessageType.TASK,
    ) -> AgentMessage:
        return AgentMessage(
            type=msg_type,
            sender=sender,
            receiver=receiver,
            content=content,
            data=data or {},
        )

    return _create


@pytest.fixture
def create_context():
    """Factory fixture to create AgentContext instances."""

    def _create(
        session_id: str = "test-session",
        shared_state: dict[str, Any] | None = None,
    ) -> AgentContext:
        ctx = AgentContext(session_id=session_id)
        if shared_state:
            for k, v in shared_state.items():
                ctx.set(k, v)
        return ctx

    return _create


# --- Pre-built agent instances ---


@pytest.fixture
def interviewer_agent():
    from backend.agents.interviewer import InterviewerAgent
    return InterviewerAgent()


@pytest.fixture
def evaluator_agent():
    from backend.agents.evaluator import EvaluatorAgent
    return EvaluatorAgent()


@pytest.fixture
def coach_agent():
    from backend.agents.coach import CoachAgent
    return CoachAgent()


@pytest.fixture
def report_agent():
    from backend.agents.report import ReportAgent
    return ReportAgent()


@pytest.fixture
def goal_tracker_agent():
    from backend.agents.goal_tracker import GoalTrackerAgent
    return GoalTrackerAgent()


@pytest.fixture
def motivator_agent():
    from backend.agents.motivator import MotivatorAgent
    return MotivatorAgent()


@pytest.fixture
def skill_monitor_agent():
    from backend.agents.skill_monitor import SkillMonitorAgent
    return SkillMonitorAgent()


@pytest.fixture
def quiz_master_agent():
    from backend.agents.quiz_master import QuizMasterAgent
    return QuizMasterAgent()


@pytest.fixture
def chatbot_agent():
    from backend.agents.chatbot import ChatBotAgent
    return ChatBotAgent()
