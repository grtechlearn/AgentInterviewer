"""
Tests for SkillMonitorAgent - 12 tests.
"""

from __future__ import annotations

import json

import pytest

from backend.agents.skill_monitor import SkillMonitorAgent, _skill_level, LEVEL_BANDS


@pytest.mark.asyncio
async def test_skill_monitor_update_skill_first_time(skill_monitor_agent, create_message, create_context):
    msg = create_message(data={"action": "update_skill", "domain": "Python", "score": 70})
    ctx = create_context()
    result = await skill_monitor_agent.process(msg, ctx)
    assert result.data["score"] == 70
    assert result.data["attempts"] == 1


@pytest.mark.asyncio
async def test_skill_monitor_update_skill_weighted_average(skill_monitor_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "skills": {"Python": {"score": 50, "attempts": 1, "history": [50], "level": "intermediate"}},
    })
    msg = create_message(data={"action": "update_skill", "domain": "Python", "score": 90})
    result = await skill_monitor_agent.process(msg, ctx)
    # 50 * 0.6 + 90 * 0.4 = 30 + 36 = 66
    assert result.data["score"] == 66
    assert result.data["attempts"] == 2


@pytest.mark.asyncio
async def test_skill_monitor_update_skill_clamped_to_100(skill_monitor_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "skills": {"Python": {"score": 95, "attempts": 5, "history": [95], "level": "advanced"}},
    })
    msg = create_message(data={"action": "update_skill", "domain": "Python", "score": 100})
    result = await skill_monitor_agent.process(msg, ctx)
    assert result.data["score"] <= 100


@pytest.mark.asyncio
async def test_skill_monitor_get_skills_empty(skill_monitor_agent, create_message, create_context):
    ctx = create_context()
    msg = create_message(data={"action": "get_skills"})
    result = await skill_monitor_agent.process(msg, ctx)
    assert result.data["skills"] == []
    assert result.data["total_domains"] == 0


@pytest.mark.asyncio
async def test_skill_monitor_get_skills_returns_all(skill_monitor_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "skills": {
            "Python": {"score": 70, "level": "intermediate", "attempts": 3, "history": []},
            "React": {"score": 40, "level": "intermediate", "attempts": 2, "history": []},
        },
    })
    msg = create_message(data={"action": "get_skills"})
    result = await skill_monitor_agent.process(msg, ctx)
    assert result.data["total_domains"] == 2
    domains = {s["domain"] for s in result.data["skills"]}
    assert domains == {"Python", "React"}


@pytest.mark.asyncio
async def test_skill_monitor_get_weak_areas_identifies_low_scores(skill_monitor_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "skills": {
            "Python": {"score": 80, "level": "advanced", "attempts": 3, "history": []},
            "React": {"score": 30, "level": "beginner", "attempts": 2, "history": []},
            "Java": {"score": 20, "level": "beginner", "attempts": 1, "history": []},
        },
    })
    msg = create_message(data={"action": "get_weak_areas"})
    result = await skill_monitor_agent.process(msg, ctx)
    assert len(result.data["weak_areas"]) == 2
    # Should be sorted by score ascending
    assert result.data["weak_areas"][0]["domain"] == "Java"


@pytest.mark.asyncio
async def test_skill_monitor_get_weak_areas_none(skill_monitor_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "skills": {
            "Python": {"score": 80, "level": "advanced", "attempts": 3, "history": []},
        },
    })
    msg = create_message(data={"action": "get_weak_areas"})
    result = await skill_monitor_agent.process(msg, ctx)
    assert len(result.data["weak_areas"]) == 0
    assert "Great work" in result.data["recommendation"]


@pytest.mark.asyncio
async def test_skill_monitor_unknown_action(skill_monitor_agent, create_message, create_context):
    msg = create_message(data={"action": "teleport"})
    ctx = create_context()
    result = await skill_monitor_agent.process(msg, ctx)
    assert "Unknown" in result.content


def test_skill_level_beginner():
    assert _skill_level(0) == "beginner"
    assert _skill_level(15) == "beginner"
    assert _skill_level(30) == "beginner"


def test_skill_level_intermediate():
    assert _skill_level(31) == "intermediate"
    assert _skill_level(50) == "intermediate"
    assert _skill_level(70) == "intermediate"


def test_skill_level_advanced():
    assert _skill_level(71) == "advanced"
    assert _skill_level(85) == "advanced"
    assert _skill_level(100) == "advanced"


def test_skill_level_out_of_range():
    # Score above 100 falls through to default
    assert _skill_level(150) == "beginner"
