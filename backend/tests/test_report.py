"""
Tests for ReportAgent - 12 tests.
"""

from __future__ import annotations

import json

import pytest

from backend.agents.report import ReportAgent, STUDY_PLANS


@pytest.mark.asyncio
async def test_report_overall_score_single_evaluation(report_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "evaluations": [{"score": 80, "question": "Q1", "correct_points": ["A"], "missing_points": ["B"]}],
        "domain": "Python",
    })
    msg = create_message()
    result = await report_agent.process(msg, ctx)
    assert result.data["overall_score"] == 80.0


@pytest.mark.asyncio
async def test_report_overall_score_multiple_evaluations(report_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "evaluations": [
            {"score": 60, "question": "Q1", "correct_points": [], "missing_points": []},
            {"score": 80, "question": "Q2", "correct_points": [], "missing_points": []},
            {"score": 100, "question": "Q3", "correct_points": [], "missing_points": []},
        ],
        "domain": "Python",
    })
    msg = create_message()
    result = await report_agent.process(msg, ctx)
    assert result.data["overall_score"] == 80.0


@pytest.mark.asyncio
async def test_report_per_question_breakdown_format(report_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "evaluations": [
            {"score": 70, "question": "Q1", "correct_points": ["A"], "missing_points": ["B"]},
            {"score": 90, "question": "Q2", "correct_points": ["C"], "missing_points": []},
        ],
        "domain": "Python",
    })
    msg = create_message()
    result = await report_agent.process(msg, ctx)
    breakdown = result.data["per_question_breakdown"]
    assert len(breakdown) == 2
    assert breakdown[0]["question_number"] == 1
    assert breakdown[1]["question_number"] == 2
    assert "score" in breakdown[0]


@pytest.mark.asyncio
async def test_report_strengths_identification(report_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "evaluations": [
            {"score": 70, "question": "Q1", "correct_points": ["Mentioned class", "Mentioned def"], "missing_points": []},
        ],
        "domain": "Python",
    })
    msg = create_message()
    result = await report_agent.process(msg, ctx)
    assert len(result.data["strengths"]) == 2


@pytest.mark.asyncio
async def test_report_weaknesses_identification(report_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "evaluations": [
            {"score": 40, "question": "Q1", "correct_points": [], "missing_points": ["Could mention GIL", "Could mention async"]},
        ],
        "domain": "Python",
    })
    msg = create_message()
    result = await report_agent.process(msg, ctx)
    assert len(result.data["weaknesses"]) == 2


@pytest.mark.asyncio
async def test_report_study_plan_present(report_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "evaluations": [{"score": 50, "question": "Q1", "correct_points": [], "missing_points": []}],
        "domain": "Python",
    })
    msg = create_message()
    result = await report_agent.process(msg, ctx)
    assert len(result.data["study_plan"]) > 0


@pytest.mark.asyncio
async def test_report_with_zero_evaluations(report_agent, create_message, create_context):
    ctx = create_context(shared_state={"evaluations": [], "domain": "Python"})
    msg = create_message()
    result = await report_agent.process(msg, ctx)
    assert result.data["overall_score"] == 0
    assert "No evaluations" in result.data["message"]


@pytest.mark.asyncio
async def test_report_with_no_evaluations_key(report_agent, create_message, create_context):
    ctx = create_context()
    msg = create_message()
    result = await report_agent.process(msg, ctx)
    assert result.data["overall_score"] == 0


@pytest.mark.asyncio
async def test_report_next_recommended_high_score(report_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "evaluations": [{"score": 90, "question": "Q1", "correct_points": [], "missing_points": []}],
        "domain": "Python",
    })
    msg = create_message()
    result = await report_agent.process(msg, ctx)
    assert "advanced" in result.data["next_recommended"].lower() or "System Design" in result.data["next_recommended"]


@pytest.mark.asyncio
async def test_report_next_recommended_low_score(report_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "evaluations": [{"score": 30, "question": "Q1", "correct_points": [], "missing_points": []}],
        "domain": "Python",
    })
    msg = create_message()
    result = await report_agent.process(msg, ctx)
    assert "fundamentals" in result.data["next_recommended"].lower()


@pytest.mark.asyncio
async def test_report_content_is_valid_json(report_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "evaluations": [{"score": 70, "question": "Q1", "correct_points": [], "missing_points": []}],
        "domain": "Python",
    })
    msg = create_message()
    result = await report_agent.process(msg, ctx)
    parsed = json.loads(result.content)
    assert "overall_score" in parsed


@pytest.mark.asyncio
async def test_report_total_questions_count(report_agent, create_message, create_context):
    evals = [{"score": 50 + i * 10, "question": f"Q{i}", "correct_points": [], "missing_points": []} for i in range(5)]
    ctx = create_context(shared_state={"evaluations": evals, "domain": "Python"})
    msg = create_message()
    result = await report_agent.process(msg, ctx)
    assert result.data["total_questions"] == 5
