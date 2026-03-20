"""
Tests for EvaluatorAgent - 17 tests.
"""

from __future__ import annotations

import json

import pytest

from backend.agents.evaluator import EvaluatorAgent, DOMAIN_KEYWORDS


@pytest.mark.asyncio
async def test_evaluator_score_for_short_answer(evaluator_agent, create_message, create_context):
    msg = create_message(data={"question": "What is Python?", "answer": "A language", "domain": "Python"})
    ctx = create_context()
    result = await evaluator_agent.process(msg, ctx)
    # Short answer should get penalized
    assert result.data["score"] <= 50


@pytest.mark.asyncio
async def test_evaluator_score_for_medium_answer(evaluator_agent, create_message, create_context):
    msg = create_message(data={
        "question": "Explain decorators",
        "answer": "A decorator is a function that wraps another function to add behavior. You use the @syntax to apply it.",
        "domain": "Python",
    })
    ctx = create_context()
    result = await evaluator_agent.process(msg, ctx)
    assert 20 <= result.data["score"] <= 80


@pytest.mark.asyncio
async def test_evaluator_score_for_long_keyword_rich_answer(evaluator_agent, create_message, create_context):
    answer = (
        "Python uses class and def to define structures. A lambda is an anonymous function. "
        "Generators use yield for lazy evaluation. Decorators wrap functions. The GIL prevents "
        "true multithreading. Async programming uses asyncio. Lists and dicts are mutable, "
        "tuples are immutable. Comprehensions provide concise syntax. You import modules."
    )
    msg = create_message(data={"question": "Explain Python", "answer": answer, "domain": "Python"})
    ctx = create_context()
    result = await evaluator_agent.process(msg, ctx)
    assert result.data["score"] >= 60


@pytest.mark.asyncio
async def test_evaluator_keyword_matching_boosts_score(evaluator_agent, create_message, create_context):
    # Answer without keywords
    msg_no_kw = create_message(data={"question": "Q", "answer": "I know some things about programming and stuff.", "domain": "Python"})
    ctx1 = create_context()
    r1 = await evaluator_agent.process(msg_no_kw, ctx1)

    # Answer with keywords
    msg_kw = create_message(data={"question": "Q", "answer": "I know class def lambda generator decorator and async patterns.", "domain": "Python"})
    ctx2 = create_context()
    r2 = await evaluator_agent.process(msg_kw, ctx2)

    assert r2.data["score"] > r1.data["score"]


@pytest.mark.asyncio
async def test_evaluator_response_has_all_fields(evaluator_agent, create_message, create_context):
    msg = create_message(data={"question": "Q", "answer": "Some answer about class and def.", "domain": "Python"})
    ctx = create_context()
    result = await evaluator_agent.process(msg, ctx)
    for key in ("score", "correct_points", "incorrect_points", "missing_points", "explanation", "difficulty_adjustment", "xp_earned", "question", "domain"):
        assert key in result.data, f"Missing key: {key}"


@pytest.mark.asyncio
async def test_evaluator_difficulty_adjustment_harder(evaluator_agent, create_message, create_context):
    answer = "class def lambda generator decorator GIL async list dict tuple yield comprehension import module " * 3
    msg = create_message(data={"question": "Q", "answer": answer, "domain": "Python"})
    ctx = create_context()
    result = await evaluator_agent.process(msg, ctx)
    # High score should suggest harder
    if result.data["score"] >= 80:
        assert result.data["difficulty_adjustment"] == "harder"


@pytest.mark.asyncio
async def test_evaluator_difficulty_adjustment_easier(evaluator_agent, create_message, create_context):
    msg = create_message(data={"question": "Q", "answer": "idk", "domain": "Python"})
    ctx = create_context()
    result = await evaluator_agent.process(msg, ctx)
    if result.data["score"] <= 40:
        assert result.data["difficulty_adjustment"] == "easier"


@pytest.mark.asyncio
async def test_evaluator_difficulty_adjustment_same(evaluator_agent, create_message, create_context):
    msg = create_message(data={"question": "Q", "answer": "Python uses class and def for structure. It has a module system.", "domain": "Python"})
    ctx = create_context()
    result = await evaluator_agent.process(msg, ctx)
    score = result.data["score"]
    if 40 < score < 80:
        assert result.data["difficulty_adjustment"] == "same"


@pytest.mark.asyncio
async def test_evaluator_xp_earned_minimum(evaluator_agent, create_message, create_context):
    msg = create_message(data={"question": "Q", "answer": "no", "domain": "Python"})
    ctx = create_context()
    result = await evaluator_agent.process(msg, ctx)
    assert result.data["xp_earned"] >= 5


@pytest.mark.asyncio
async def test_evaluator_xp_earned_scales_with_score(evaluator_agent, create_message, create_context):
    answer_low = "um"
    answer_high = "class def lambda generator decorator GIL async list dict tuple yield comprehension import module " * 2
    ctx1 = create_context()
    ctx2 = create_context()
    r1 = await evaluator_agent.process(create_message(data={"question": "Q", "answer": answer_low, "domain": "Python"}), ctx1)
    r2 = await evaluator_agent.process(create_message(data={"question": "Q", "answer": answer_high, "domain": "Python"}), ctx2)
    assert r2.data["xp_earned"] >= r1.data["xp_earned"]


@pytest.mark.asyncio
async def test_evaluator_stores_evaluation_in_context(evaluator_agent, create_message, create_context):
    msg = create_message(data={"question": "Q", "answer": "class stuff", "domain": "Python"})
    ctx = create_context()
    await evaluator_agent.process(msg, ctx)
    evals = ctx.get("evaluations")
    assert isinstance(evals, list)
    assert len(evals) == 1


@pytest.mark.asyncio
async def test_evaluator_stores_last_evaluation(evaluator_agent, create_message, create_context):
    msg = create_message(data={"question": "Q", "answer": "class stuff", "domain": "Python"})
    ctx = create_context()
    await evaluator_agent.process(msg, ctx)
    last = ctx.get("last_evaluation")
    assert last is not None
    assert "score" in last


@pytest.mark.asyncio
async def test_evaluator_with_missing_question_data(evaluator_agent, create_message, create_context):
    msg = create_message(data={})
    ctx = create_context()
    result = await evaluator_agent.process(msg, ctx)
    # Should handle gracefully with defaults
    assert "score" in result.data


@pytest.mark.asyncio
async def test_evaluator_content_is_valid_json(evaluator_agent, create_message, create_context):
    msg = create_message(data={"question": "Q", "answer": "A", "domain": "Python"})
    ctx = create_context()
    result = await evaluator_agent.process(msg, ctx)
    parsed = json.loads(result.content)
    assert "score" in parsed


def test_evaluator_explanation_excellent(evaluator_agent):
    assert "Excellent" in evaluator_agent._build_explanation(85)


def test_evaluator_explanation_good(evaluator_agent):
    assert "Good" in evaluator_agent._build_explanation(65)


def test_evaluator_explanation_needs_improvement(evaluator_agent):
    assert "improvement" in evaluator_agent._build_explanation(20).lower()


def test_domain_keywords_has_all_domains():
    expected = {"Python", "JavaScript", "React", "iOS", "Android", "ReactNative", "Java", "DevOps", "SystemDesign", "HR"}
    assert set(DOMAIN_KEYWORDS.keys()) == expected
