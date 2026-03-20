"""
Tests for MultiRoundAgent - 13 tests.
"""

from __future__ import annotations

import json

import pytest

from backend.agents.multi_round import MultiRoundAgent, ROUNDS, TOTAL_ROUNDS


@pytest.mark.asyncio
async def test_start_pipeline_returns_first_round(multi_round_agent, create_message, create_context):
    msg = create_message(data={"action": "start_pipeline"})
    ctx = create_context()
    result = await multi_round_agent.process(msg, ctx)
    assert result.data["status"] == "pipeline_started"
    assert result.data["round_name"] == "phone_screen"
    assert result.data["difficulty"] == "easy"


@pytest.mark.asyncio
async def test_start_pipeline_initializes_context(multi_round_agent, create_message, create_context):
    msg = create_message(data={"action": "start_pipeline"})
    ctx = create_context()
    await multi_round_agent.process(msg, ctx)
    assert ctx.get("pipeline_round") == 0
    assert ctx.get("pipeline_scores") == {}
    assert ctx.get("pipeline_started") is True


@pytest.mark.asyncio
async def test_start_pipeline_progress_is_zero(multi_round_agent, create_message, create_context):
    msg = create_message(data={"action": "start_pipeline"})
    ctx = create_context()
    result = await multi_round_agent.process(msg, ctx)
    assert result.data["overall_progress"] == 0


@pytest.mark.asyncio
async def test_next_round_advances(multi_round_agent, create_message, create_context):
    ctx = create_context(shared_state={"pipeline_round": 0, "pipeline_scores": {}, "pipeline_started": True})
    msg = create_message(data={"action": "next_round", "round_score": 85})
    result = await multi_round_agent.process(msg, ctx)
    assert result.data["round_name"] == "technical"
    assert result.data["current_round"] == 1


@pytest.mark.asyncio
async def test_next_round_stores_score(multi_round_agent, create_message, create_context):
    ctx = create_context(shared_state={"pipeline_round": 0, "pipeline_scores": {}, "pipeline_started": True})
    msg = create_message(data={"action": "next_round", "round_score": 90})
    await multi_round_agent.process(msg, ctx)
    scores = ctx.get("pipeline_scores")
    assert scores["phone_screen"] == 90


@pytest.mark.asyncio
async def test_next_round_progress_increases(multi_round_agent, create_message, create_context):
    ctx = create_context(shared_state={"pipeline_round": 1, "pipeline_scores": {"phone_screen": 80}, "pipeline_started": True})
    msg = create_message(data={"action": "next_round", "round_score": 75})
    result = await multi_round_agent.process(msg, ctx)
    assert result.data["overall_progress"] > 0


@pytest.mark.asyncio
async def test_next_round_completes_pipeline(multi_round_agent, create_message, create_context):
    scores = {r["name"]: 80 for r in ROUNDS[:4]}
    ctx = create_context(shared_state={"pipeline_round": 4, "pipeline_scores": scores, "pipeline_started": True})
    msg = create_message(data={"action": "next_round", "round_score": 85})
    result = await multi_round_agent.process(msg, ctx)
    assert result.data["status"] == "pipeline_complete"
    assert result.data["overall_progress"] == 100


@pytest.mark.asyncio
async def test_get_status_not_started(multi_round_agent, create_message, create_context):
    ctx = create_context()
    msg = create_message(data={"action": "get_pipeline_status"})
    result = await multi_round_agent.process(msg, ctx)
    assert result.data["status"] == "not_started"


@pytest.mark.asyncio
async def test_get_status_in_progress(multi_round_agent, create_message, create_context):
    ctx = create_context(shared_state={"pipeline_round": 2, "pipeline_scores": {"phone_screen": 80, "technical": 70}, "pipeline_started": True})
    msg = create_message(data={"action": "get_pipeline_status"})
    result = await multi_round_agent.process(msg, ctx)
    assert result.data["status"] == "in_progress"
    assert result.data["round_name"] == "system_design"
    assert len(result.data["completed_rounds"]) == 2


@pytest.mark.asyncio
async def test_pipeline_report_partial(multi_round_agent, create_message, create_context):
    ctx = create_context(shared_state={"pipeline_round": 1, "pipeline_scores": {"phone_screen": 90}, "pipeline_started": True})
    msg = create_message(data={"action": "pipeline_report"})
    result = await multi_round_agent.process(msg, ctx)
    assert result.data["rounds_completed"] == 1
    assert result.data["total_rounds"] == TOTAL_ROUNDS
    assert "incomplete" in result.data["recommendation"].lower()


@pytest.mark.asyncio
async def test_pipeline_report_full_high_score(multi_round_agent, create_message, create_context):
    scores = {r["name"]: 85 for r in ROUNDS}
    ctx = create_context(shared_state={"pipeline_round": 4, "pipeline_scores": scores, "pipeline_started": True})
    msg = create_message(data={"action": "pipeline_report"})
    result = await multi_round_agent.process(msg, ctx)
    assert result.data["rounds_completed"] == TOTAL_ROUNDS
    assert "offer" in result.data["recommendation"].lower()


@pytest.mark.asyncio
async def test_unknown_action_returns_error(multi_round_agent, create_message, create_context):
    msg = create_message(data={"action": "fly_away"})
    ctx = create_context()
    result = await multi_round_agent.process(msg, ctx)
    assert "Unknown action" in result.content


@pytest.mark.asyncio
async def test_content_is_valid_json(multi_round_agent, create_message, create_context):
    msg = create_message(data={"action": "start_pipeline"})
    ctx = create_context()
    result = await multi_round_agent.process(msg, ctx)
    parsed = json.loads(result.content)
    assert parsed["round_name"] == "phone_screen"
