"""
Tests for QuizMasterAgent - 12 tests.
"""

from __future__ import annotations

import json

import pytest

from backend.agents.quiz_master import QuizMasterAgent, QUIZ_BANK


@pytest.mark.asyncio
async def test_quiz_master_start_quiz_returns_question(quiz_master_agent, create_message, create_context):
    msg = create_message(data={"action": "start_quiz", "domain": "Python"})
    ctx = create_context()
    result = await quiz_master_agent.process(msg, ctx)
    assert "question" in result.data
    assert "options" in result.data
    assert result.data["question_number"] == 1


@pytest.mark.asyncio
async def test_quiz_master_start_quiz_has_4_options(quiz_master_agent, create_message, create_context):
    msg = create_message(data={"action": "start_quiz", "domain": "Python"})
    ctx = create_context()
    result = await quiz_master_agent.process(msg, ctx)
    assert len(result.data["options"]) == 4


@pytest.mark.asyncio
async def test_quiz_master_start_quiz_javascript(quiz_master_agent, create_message, create_context):
    msg = create_message(data={"action": "start_quiz", "domain": "JavaScript"})
    ctx = create_context()
    result = await quiz_master_agent.process(msg, ctx)
    assert result.data["domain"] == "JavaScript"


@pytest.mark.asyncio
async def test_quiz_master_submit_correct_answer(quiz_master_agent, create_message, create_context):
    # Start quiz first
    start_msg = create_message(data={"action": "start_quiz", "domain": "Python"})
    ctx = create_context()
    start_result = await quiz_master_agent.process(start_msg, ctx)

    # Get the correct answer from context
    questions = ctx.get("quiz_questions")
    correct_answer = questions[0]["answer"]

    submit_msg = create_message(data={"action": "submit_answer", "answer": correct_answer})
    result = await quiz_master_agent.process(submit_msg, ctx)
    assert result.data["is_correct"] is True
    assert result.data["current_score"] == 1


@pytest.mark.asyncio
async def test_quiz_master_submit_incorrect_answer(quiz_master_agent, create_message, create_context):
    start_msg = create_message(data={"action": "start_quiz", "domain": "Python"})
    ctx = create_context()
    await quiz_master_agent.process(start_msg, ctx)

    submit_msg = create_message(data={"action": "submit_answer", "answer": "DEFINITELY_WRONG"})
    result = await quiz_master_agent.process(submit_msg, ctx)
    assert result.data["is_correct"] is False
    assert result.data["current_score"] == 0


@pytest.mark.asyncio
async def test_quiz_master_submit_answer_shows_next_question(quiz_master_agent, create_message, create_context):
    start_msg = create_message(data={"action": "start_quiz", "domain": "Python"})
    ctx = create_context()
    await quiz_master_agent.process(start_msg, ctx)

    submit_msg = create_message(data={"action": "submit_answer", "answer": "wrong"})
    result = await quiz_master_agent.process(submit_msg, ctx)
    assert "next_question" in result.data
    assert result.data["next_question"]["question_number"] == 2


@pytest.mark.asyncio
async def test_quiz_master_complete_quiz(quiz_master_agent, create_message, create_context):
    start_msg = create_message(data={"action": "start_quiz", "domain": "Python"})
    ctx = create_context()
    await quiz_master_agent.process(start_msg, ctx)

    questions = ctx.get("quiz_questions")
    # Answer all questions
    for i in range(len(questions)):
        submit_msg = create_message(data={"action": "submit_answer", "answer": "wrong"})
        result = await quiz_master_agent.process(submit_msg, ctx)

    assert result.data["quiz_complete"] is True
    assert result.data["final_score"] == 0
    assert result.data["percentage"] == 0


@pytest.mark.asyncio
async def test_quiz_master_get_results(quiz_master_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "quiz_questions": QUIZ_BANK["Python"][:3],
        "quiz_score": 2,
        "quiz_answers": [
            {"question": "Q1", "user_answer": "A", "correct_answer": "A", "is_correct": True},
            {"question": "Q2", "user_answer": "B", "correct_answer": "B", "is_correct": True},
            {"question": "Q3", "user_answer": "X", "correct_answer": "C", "is_correct": False},
        ],
        "quiz_domain": "Python",
    })
    msg = create_message(data={"action": "get_results"})
    result = await quiz_master_agent.process(msg, ctx)
    assert result.data["final_score"] == 2
    assert result.data["total"] == 3
    assert result.data["percentage"] == 67


@pytest.mark.asyncio
async def test_quiz_master_get_results_empty(quiz_master_agent, create_message, create_context):
    ctx = create_context()
    msg = create_message(data={"action": "get_results"})
    result = await quiz_master_agent.process(msg, ctx)
    assert result.data["final_score"] == 0
    assert result.data["percentage"] == 0


@pytest.mark.asyncio
async def test_quiz_master_unknown_action(quiz_master_agent, create_message, create_context):
    msg = create_message(data={"action": "cheat"})
    ctx = create_context()
    result = await quiz_master_agent.process(msg, ctx)
    assert "Unknown" in result.content


def test_quiz_bank_python_has_questions():
    assert len(QUIZ_BANK["Python"]) >= 5


def test_quiz_bank_javascript_has_questions():
    assert len(QUIZ_BANK["JavaScript"]) >= 5
