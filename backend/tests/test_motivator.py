"""
Tests for MotivatorAgent - 11 tests.
"""

from __future__ import annotations

import json

import pytest

from backend.agents.motivator import MotivatorAgent, DAILY_MESSAGES, TOPICS_OF_DAY, MILESTONES


@pytest.mark.asyncio
async def test_motivator_daily_message_returns_non_empty(motivator_agent, create_message, create_context):
    msg = create_message(data={"action": "daily_message"})
    ctx = create_context()
    result = await motivator_agent.process(msg, ctx)
    assert len(result.data["message"]) > 0


@pytest.mark.asyncio
async def test_motivator_daily_message_includes_streak(motivator_agent, create_message, create_context):
    ctx = create_context(shared_state={"streak": 7})
    msg = create_message(data={"action": "daily_message"})
    result = await motivator_agent.process(msg, ctx)
    assert result.data["streak"] == 7


@pytest.mark.asyncio
async def test_motivator_daily_message_includes_date(motivator_agent, create_message, create_context):
    msg = create_message(data={"action": "daily_message"})
    ctx = create_context()
    result = await motivator_agent.process(msg, ctx)
    assert "date" in result.data
    assert len(result.data["date"]) == 10  # YYYY-MM-DD


@pytest.mark.asyncio
async def test_motivator_topic_of_day_returns_topic(motivator_agent, create_message, create_context):
    msg = create_message(data={"action": "topic_of_day"})
    ctx = create_context()
    result = await motivator_agent.process(msg, ctx)
    assert "topic_of_day" in result.data
    assert "domain" in result.data
    assert "why" in result.data


def test_motivator_topic_of_day_rotates():
    """Verify different days produce different topics (mod len)."""
    topics = [TOPICS_OF_DAY[i % len(TOPICS_OF_DAY)]["topic"] for i in range(len(TOPICS_OF_DAY))]
    # All topics should appear at least once
    unique = set(topics)
    assert len(unique) == len(TOPICS_OF_DAY)


@pytest.mark.asyncio
async def test_motivator_celebrate_milestone_10_questions(motivator_agent, create_message, create_context):
    evals = [{"score": 50} for _ in range(10)]
    ctx = create_context(shared_state={"evaluations": evals, "streak": 0})
    msg = create_message(data={"action": "celebrate_milestone"})
    result = await motivator_agent.process(msg, ctx)
    assert any("10" in c for c in result.data["celebrations"])


@pytest.mark.asyncio
async def test_motivator_celebrate_milestone_7_streak(motivator_agent, create_message, create_context):
    ctx = create_context(shared_state={"evaluations": [], "streak": 7})
    msg = create_message(data={"action": "celebrate_milestone"})
    result = await motivator_agent.process(msg, ctx)
    assert any("7-day" in c for c in result.data["celebrations"])


@pytest.mark.asyncio
async def test_motivator_celebrate_no_milestone(motivator_agent, create_message, create_context):
    ctx = create_context(shared_state={"evaluations": [{"score": 50} for _ in range(3)], "streak": 2})
    msg = create_message(data={"action": "celebrate_milestone"})
    result = await motivator_agent.process(msg, ctx)
    assert any("Keep going" in c for c in result.data["celebrations"])


@pytest.mark.asyncio
async def test_motivator_unknown_action(motivator_agent, create_message, create_context):
    msg = create_message(data={"action": "sing"})
    ctx = create_context()
    result = await motivator_agent.process(msg, ctx)
    assert "Unknown" in result.content


@pytest.mark.asyncio
async def test_motivator_daily_message_from_pool(motivator_agent, create_message, create_context):
    msg = create_message(data={"action": "daily_message"})
    ctx = create_context()
    result = await motivator_agent.process(msg, ctx)
    assert result.data["message"] in DAILY_MESSAGES


@pytest.mark.asyncio
async def test_motivator_content_is_valid_json(motivator_agent, create_message, create_context):
    msg = create_message(data={"action": "daily_message"})
    ctx = create_context()
    result = await motivator_agent.process(msg, ctx)
    parsed = json.loads(result.content)
    assert "message" in parsed
