"""
Tests for CoachAgent - 12 tests.
"""

from __future__ import annotations

import json

import pytest

from backend.agents.coach import CoachAgent, TIPS_BY_DOMAIN, RESOURCES


@pytest.mark.asyncio
async def test_coach_tips_from_evaluation_context(coach_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "last_evaluation": {"domain": "Python", "score": 60},
        "domain": "Python",
        "topics_covered": ["Data Structures"],
    })
    msg = create_message()
    result = await coach_agent.process(msg, ctx)
    assert "tips" in result.data
    assert len(result.data["tips"]) > 0


@pytest.mark.asyncio
async def test_coach_resources_not_empty(coach_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "last_evaluation": {"domain": "Python", "score": 50},
        "domain": "Python",
    })
    msg = create_message()
    result = await coach_agent.process(msg, ctx)
    assert len(result.data["resources"]) > 0


@pytest.mark.asyncio
async def test_coach_motivation_message_high_score(coach_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "last_evaluation": {"domain": "Python", "score": 90},
    })
    msg = create_message()
    result = await coach_agent.process(msg, ctx)
    assert "Outstanding" in result.data["motivation_message"]


@pytest.mark.asyncio
async def test_coach_motivation_message_medium_score(coach_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "last_evaluation": {"domain": "Python", "score": 65},
    })
    msg = create_message()
    result = await coach_agent.process(msg, ctx)
    assert "Great progress" in result.data["motivation_message"]


@pytest.mark.asyncio
async def test_coach_motivation_message_low_score(coach_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "last_evaluation": {"domain": "Python", "score": 45},
    })
    msg = create_message()
    result = await coach_agent.process(msg, ctx)
    assert "Good effort" in result.data["motivation_message"]


@pytest.mark.asyncio
async def test_coach_motivation_message_very_low_score(coach_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "last_evaluation": {"domain": "Python", "score": 20},
    })
    msg = create_message()
    result = await coach_agent.process(msg, ctx)
    assert "beginner" in result.data["motivation_message"]


@pytest.mark.asyncio
async def test_coach_handles_missing_evaluation(coach_agent, create_message, create_context):
    ctx = create_context()
    msg = create_message()
    result = await coach_agent.process(msg, ctx)
    # Should still return a valid response with defaults
    assert "tips" in result.data
    assert "motivation_message" in result.data


@pytest.mark.asyncio
async def test_coach_next_topic_suggestion_from_remaining(coach_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "last_evaluation": {"domain": "Python", "score": 50},
        "domain": "Python",
        "topics_covered": ["Data Structures"],
    })
    msg = create_message()
    result = await coach_agent.process(msg, ctx)
    assert result.data["next_topic_suggestion"] != "Data Structures"


@pytest.mark.asyncio
async def test_coach_content_is_valid_json(coach_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "last_evaluation": {"domain": "Python", "score": 50},
    })
    msg = create_message()
    result = await coach_agent.process(msg, ctx)
    parsed = json.loads(result.content)
    assert "tips" in parsed


@pytest.mark.asyncio
async def test_coach_result_contains_domain(coach_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "last_evaluation": {"domain": "React", "score": 70},
    })
    msg = create_message()
    result = await coach_agent.process(msg, ctx)
    assert result.data["domain"] == "React"


@pytest.mark.asyncio
async def test_coach_tips_for_unknown_domain_falls_back(coach_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "last_evaluation": {"domain": "Rust", "score": 50},
    })
    msg = create_message()
    result = await coach_agent.process(msg, ctx)
    # Falls back to Python tips
    assert result.data["tips"] == TIPS_BY_DOMAIN["Python"][:3]


@pytest.mark.asyncio
async def test_coach_current_score_in_result(coach_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "last_evaluation": {"domain": "Python", "score": 77},
    })
    msg = create_message()
    result = await coach_agent.process(msg, ctx)
    assert result.data["current_score"] == 77
