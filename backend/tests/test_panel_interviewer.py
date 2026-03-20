"""
Tests for PanelInterviewerAgent - 12 tests.
"""

from __future__ import annotations

import json

import pytest

from backend.agents.panel_interviewer import PanelInterviewerAgent, PERSONAS


@pytest.mark.asyncio
async def test_start_panel_returns_panel_info(panel_interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "start_panel"})
    ctx = create_context()
    result = await panel_interviewer_agent.process(msg, ctx)
    assert result.data["status"] == "panel_started"
    assert result.data["total_personas"] == 3


@pytest.mark.asyncio
async def test_start_panel_initializes_context(panel_interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "start_panel"})
    ctx = create_context()
    await panel_interviewer_agent.process(msg, ctx)
    assert ctx.get("panel_index") == 0
    assert ctx.get("panel_question_num") == 0
    assert ctx.get("panel_scores") == []


@pytest.mark.asyncio
async def test_panel_question_returns_first_persona(panel_interviewer_agent, create_message, create_context):
    ctx = create_context(shared_state={"panel_question_num": 0, "panel_index": 0})
    msg = create_message(data={"action": "panel_question"})
    result = await panel_interviewer_agent.process(msg, ctx)
    assert result.data["persona_name"] == PERSONAS[0]["name"]
    assert result.data["persona_role"] == PERSONAS[0]["role"]


@pytest.mark.asyncio
async def test_panel_question_rotates_personas(panel_interviewer_agent, create_message, create_context):
    ctx = create_context(shared_state={"panel_question_num": 0, "panel_index": 0})

    names = []
    for _ in range(3):
        msg = create_message(data={"action": "panel_question"})
        result = await panel_interviewer_agent.process(msg, ctx)
        names.append(result.data["persona_name"])

    assert names[0] == PERSONAS[0]["name"]
    assert names[1] == PERSONAS[1]["name"]
    assert names[2] == PERSONAS[2]["name"]


@pytest.mark.asyncio
async def test_panel_question_increments_counter(panel_interviewer_agent, create_message, create_context):
    ctx = create_context(shared_state={"panel_question_num": 0, "panel_index": 0})
    msg = create_message(data={"action": "panel_question"})
    await panel_interviewer_agent.process(msg, ctx)
    assert ctx.get("panel_question_num") == 1


@pytest.mark.asyncio
async def test_panel_question_has_required_keys(panel_interviewer_agent, create_message, create_context):
    ctx = create_context(shared_state={"panel_question_num": 0, "panel_index": 0})
    msg = create_message(data={"action": "panel_question"})
    result = await panel_interviewer_agent.process(msg, ctx)
    for key in ("question", "persona_name", "persona_role", "focus_area"):
        assert key in result.data, f"Missing key: {key}"


@pytest.mark.asyncio
async def test_panel_evaluate_returns_score(panel_interviewer_agent, create_message, create_context):
    ctx = create_context(shared_state={"panel_index": 0, "panel_scores": []})
    msg = create_message(data={"action": "panel_evaluate", "answer": "This is a detailed answer about design patterns and architecture."})
    result = await panel_interviewer_agent.process(msg, ctx)
    assert "score" in result.data
    assert 0 <= result.data["score"] <= 100


@pytest.mark.asyncio
async def test_panel_evaluate_stores_score_in_context(panel_interviewer_agent, create_message, create_context):
    ctx = create_context(shared_state={"panel_index": 0, "panel_scores": []})
    msg = create_message(data={"action": "panel_evaluate", "answer": "Good answer."})
    await panel_interviewer_agent.process(msg, ctx)
    scores = ctx.get("panel_scores")
    assert len(scores) == 1
    assert scores[0]["persona_name"] == PERSONAS[0]["name"]


@pytest.mark.asyncio
async def test_panel_evaluate_brief_answer_lower_score(panel_interviewer_agent, create_message, create_context):
    ctx = create_context(shared_state={"panel_index": 0, "panel_scores": []})
    msg = create_message(data={"action": "panel_evaluate", "answer": "ok"})
    result = await panel_interviewer_agent.process(msg, ctx)
    assert result.data["score"] <= 70


@pytest.mark.asyncio
async def test_panel_evaluate_computes_average(panel_interviewer_agent, create_message, create_context):
    existing = [{"persona_name": "A", "persona_role": "R", "score": 80, "feedback": "Good"}]
    ctx = create_context(shared_state={"panel_index": 1, "panel_scores": existing})
    msg = create_message(data={"action": "panel_evaluate", "answer": "Detailed response about system architecture."})
    result = await panel_interviewer_agent.process(msg, ctx)
    assert result.data["total_evaluations"] == 2
    assert "average_score" in result.data


@pytest.mark.asyncio
async def test_panel_unknown_action_returns_error(panel_interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "unknown_action"})
    ctx = create_context()
    result = await panel_interviewer_agent.process(msg, ctx)
    assert "Unknown action" in result.content


@pytest.mark.asyncio
async def test_panel_content_is_valid_json(panel_interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "start_panel"})
    ctx = create_context()
    result = await panel_interviewer_agent.process(msg, ctx)
    parsed = json.loads(result.content)
    assert parsed["status"] == "panel_started"
