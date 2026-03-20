"""
Tests for GoalTrackerAgent - 12 tests.
"""

from __future__ import annotations

import json

import pytest

from backend.agents.goal_tracker import GoalTrackerAgent


@pytest.mark.asyncio
async def test_goal_tracker_set_goal_stores_in_context(goal_tracker_agent, create_message, create_context):
    msg = create_message(data={"action": "set_goal", "domain": "Python", "daily_questions": 10, "target_score": 80})
    ctx = create_context()
    result = await goal_tracker_agent.process(msg, ctx)
    assert result.data["status"] == "goal_set"
    goals = ctx.get("goals")
    assert len(goals) == 1
    assert goals[0]["daily_questions"] == 10


@pytest.mark.asyncio
async def test_goal_tracker_set_goal_defaults(goal_tracker_agent, create_message, create_context):
    msg = create_message(data={"action": "set_goal"})
    ctx = create_context()
    result = await goal_tracker_agent.process(msg, ctx)
    goal = result.data["goal"]
    assert goal["daily_questions"] == 5
    assert goal["weekly_target"] == 25
    assert goal["target_score"] == 70


@pytest.mark.asyncio
async def test_goal_tracker_get_progress_empty(goal_tracker_agent, create_message, create_context):
    msg = create_message(data={"action": "get_progress"})
    ctx = create_context()
    result = await goal_tracker_agent.process(msg, ctx)
    assert result.data["questions_completed"] == 0
    assert result.data["average_score"] == 0.0
    assert result.data["current_streak"] == 0


@pytest.mark.asyncio
async def test_goal_tracker_get_progress_with_evaluations(goal_tracker_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "evaluations": [{"score": 70}, {"score": 90}],
        "streak": 5,
        "goals": [{"daily_questions": 5, "target_score": 70}],
    })
    msg = create_message(data={"action": "get_progress"})
    result = await goal_tracker_agent.process(msg, ctx)
    assert result.data["questions_completed"] == 2
    assert result.data["average_score"] == 80.0
    assert result.data["on_track"] is True


@pytest.mark.asyncio
async def test_goal_tracker_get_progress_not_on_track(goal_tracker_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "evaluations": [{"score": 30}, {"score": 40}],
        "goals": [{"daily_questions": 5, "target_score": 70}],
    })
    msg = create_message(data={"action": "get_progress"})
    result = await goal_tracker_agent.process(msg, ctx)
    assert result.data["on_track"] is False


@pytest.mark.asyncio
async def test_goal_tracker_update_streak(goal_tracker_agent, create_message, create_context):
    ctx = create_context(shared_state={"streak": 3, "best_streak": 5})
    msg = create_message(data={"action": "update_streak"})
    result = await goal_tracker_agent.process(msg, ctx)
    assert result.data["current_streak"] == 4
    assert result.data["best_streak"] == 5
    assert result.data["streak_updated"] is True


@pytest.mark.asyncio
async def test_goal_tracker_update_streak_new_best(goal_tracker_agent, create_message, create_context):
    ctx = create_context(shared_state={"streak": 5, "best_streak": 5})
    msg = create_message(data={"action": "update_streak"})
    result = await goal_tracker_agent.process(msg, ctx)
    assert result.data["current_streak"] == 6
    assert result.data["best_streak"] == 6


@pytest.mark.asyncio
async def test_goal_tracker_check_daily_not_complete(goal_tracker_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "evaluations": [{"score": 50}, {"score": 60}],
        "goals": [{"daily_questions": 5}],
    })
    msg = create_message(data={"action": "check_daily"})
    result = await goal_tracker_agent.process(msg, ctx)
    assert result.data["daily_complete"] is False
    assert result.data["remaining"] == 3


@pytest.mark.asyncio
async def test_goal_tracker_check_daily_complete(goal_tracker_agent, create_message, create_context):
    evals = [{"score": 50 + i} for i in range(5)]
    ctx = create_context(shared_state={
        "evaluations": evals,
        "goals": [{"daily_questions": 5}],
    })
    msg = create_message(data={"action": "check_daily"})
    result = await goal_tracker_agent.process(msg, ctx)
    assert result.data["daily_complete"] is True
    assert result.data["remaining"] == 0
    assert "Great job" in result.data["message"]


@pytest.mark.asyncio
async def test_goal_tracker_check_daily_default_target(goal_tracker_agent, create_message, create_context):
    ctx = create_context()
    msg = create_message(data={"action": "check_daily"})
    result = await goal_tracker_agent.process(msg, ctx)
    assert result.data["daily_target"] == 5


@pytest.mark.asyncio
async def test_goal_tracker_unknown_action(goal_tracker_agent, create_message, create_context):
    msg = create_message(data={"action": "fly"})
    ctx = create_context()
    result = await goal_tracker_agent.process(msg, ctx)
    assert "Unknown" in result.content


@pytest.mark.asyncio
async def test_goal_tracker_daily_progress_percentage(goal_tracker_agent, create_message, create_context):
    evals = [{"score": 50} for _ in range(3)]
    ctx = create_context(shared_state={
        "evaluations": evals,
        "goals": [{"daily_questions": 10, "target_score": 70}],
    })
    msg = create_message(data={"action": "get_progress"})
    result = await goal_tracker_agent.process(msg, ctx)
    assert result.data["daily_progress_pct"] == 30
