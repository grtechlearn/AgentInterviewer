"""
Tests for InterviewerAgent - 22 tests.
"""

from __future__ import annotations

import json

import pytest

from backend.agents.interviewer import InterviewerAgent, MOCK_QUESTIONS, DIFFICULTY_MAP


@pytest.mark.asyncio
async def test_interviewer_start_python_returns_question(interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "start_interview", "domain": "Python"})
    ctx = create_context()
    result = await interviewer_agent.process(msg, ctx)
    data = result.data
    assert "question" in data
    assert data["domain"] == "Python"


@pytest.mark.asyncio
async def test_interviewer_start_react_returns_question(interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "start_interview", "domain": "React"})
    ctx = create_context()
    result = await interviewer_agent.process(msg, ctx)
    assert result.data["domain"] == "React"
    assert result.data["question"] in [q["question"] for q in MOCK_QUESTIONS["React"]]


@pytest.mark.asyncio
async def test_interviewer_start_ios_returns_question(interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "start_interview", "domain": "iOS"})
    ctx = create_context()
    result = await interviewer_agent.process(msg, ctx)
    assert result.data["domain"] == "iOS"


@pytest.mark.asyncio
async def test_interviewer_start_android_returns_question(interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "start_interview", "domain": "Android"})
    ctx = create_context()
    result = await interviewer_agent.process(msg, ctx)
    assert result.data["domain"] == "Android"


@pytest.mark.asyncio
async def test_interviewer_start_java_returns_question(interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "start_interview", "domain": "Java"})
    ctx = create_context()
    result = await interviewer_agent.process(msg, ctx)
    assert result.data["domain"] == "Java"


@pytest.mark.asyncio
async def test_interviewer_start_javascript_returns_question(interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "start_interview", "domain": "JavaScript"})
    ctx = create_context()
    result = await interviewer_agent.process(msg, ctx)
    assert result.data["domain"] == "JavaScript"


@pytest.mark.asyncio
async def test_interviewer_start_devops_returns_question(interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "start_interview", "domain": "DevOps"})
    ctx = create_context()
    result = await interviewer_agent.process(msg, ctx)
    assert result.data["domain"] == "DevOps"


@pytest.mark.asyncio
async def test_interviewer_start_systemdesign_returns_question(interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "start_interview", "domain": "SystemDesign"})
    ctx = create_context()
    result = await interviewer_agent.process(msg, ctx)
    assert result.data["domain"] == "SystemDesign"


@pytest.mark.asyncio
async def test_interviewer_start_hr_returns_question(interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "start_interview", "domain": "HR"})
    ctx = create_context()
    result = await interviewer_agent.process(msg, ctx)
    assert result.data["domain"] == "HR"


@pytest.mark.asyncio
async def test_interviewer_start_reactnative_returns_question(interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "start_interview", "domain": "ReactNative"})
    ctx = create_context()
    result = await interviewer_agent.process(msg, ctx)
    assert result.data["domain"] == "ReactNative"


@pytest.mark.asyncio
async def test_interviewer_start_sets_context_state(interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "start_interview", "domain": "Python", "total_questions": 10})
    ctx = create_context()
    await interviewer_agent.process(msg, ctx)
    assert ctx.get("domain") == "Python"
    assert ctx.get("current_question") == 1
    assert ctx.get("total_questions") == 10
    assert isinstance(ctx.get("topics_covered"), list)


@pytest.mark.asyncio
async def test_interviewer_next_question_increments_counter(interviewer_agent, create_message, create_context):
    ctx = create_context(shared_state={"domain": "Python", "difficulty": "medium", "current_question": 1, "total_questions": 5, "topics_covered": []})
    msg = create_message(data={"action": "next_question"})
    result = await interviewer_agent.process(msg, ctx)
    assert ctx.get("current_question") == 2
    assert result.data["question_number"] == 2


@pytest.mark.asyncio
async def test_interviewer_next_question_avoids_topic_repetition(interviewer_agent, create_message, create_context):
    # Cover all but one topic to force selection of the remaining one
    all_topics = [q["topic"] for q in MOCK_QUESTIONS["Python"]]
    unique_topics = list(set(all_topics))
    covered = unique_topics[:-1]
    remaining_topic = unique_topics[-1]

    ctx = create_context(shared_state={
        "domain": "Python", "difficulty": "medium",
        "current_question": 1, "total_questions": 5,
        "topics_covered": covered,
    })
    msg = create_message(data={"action": "next_question"})
    result = await interviewer_agent.process(msg, ctx)
    assert result.data["topic"] == remaining_topic


@pytest.mark.asyncio
async def test_interviewer_follow_up_action(interviewer_agent, create_message, create_context):
    ctx = create_context(shared_state={
        "domain": "Python", "difficulty": "hard",
        "current_question": 2, "total_questions": 5,
        "topics_covered": ["Data Structures", "Functions"],
    })
    msg = create_message(data={"action": "follow_up"})
    result = await interviewer_agent.process(msg, ctx)
    assert result.data["is_follow_up"] is True
    assert "Functions" in result.data["question"]


@pytest.mark.asyncio
async def test_interviewer_difficulty_easy(interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "start_interview", "domain": "Python", "difficulty": "easy"})
    ctx = create_context()
    result = await interviewer_agent.process(msg, ctx)
    assert result.data["difficulty"] == "easy"


@pytest.mark.asyncio
async def test_interviewer_difficulty_hard(interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "start_interview", "domain": "Python", "difficulty": "hard"})
    ctx = create_context()
    result = await interviewer_agent.process(msg, ctx)
    assert result.data["difficulty"] == "hard"


@pytest.mark.asyncio
async def test_interviewer_question_format_has_required_keys(interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "start_interview", "domain": "Python"})
    ctx = create_context()
    result = await interviewer_agent.process(msg, ctx)
    for key in ("question", "topic", "difficulty", "question_number", "total_questions", "hint", "domain"):
        assert key in result.data, f"Missing key: {key}"


@pytest.mark.asyncio
async def test_interviewer_unknown_domain_falls_back_to_python(interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "start_interview", "domain": "Rust"})
    ctx = create_context()
    result = await interviewer_agent.process(msg, ctx)
    # Falls back to Python questions
    assert result.data["question"] in [q["question"] for q in MOCK_QUESTIONS["Python"]]


@pytest.mark.asyncio
async def test_interviewer_unknown_action_returns_error(interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "dance"})
    ctx = create_context()
    result = await interviewer_agent.process(msg, ctx)
    assert "Unknown action" in result.content


@pytest.mark.asyncio
async def test_interviewer_content_is_valid_json(interviewer_agent, create_message, create_context):
    msg = create_message(data={"action": "start_interview", "domain": "Python"})
    ctx = create_context()
    result = await interviewer_agent.process(msg, ctx)
    parsed = json.loads(result.content)
    assert parsed["domain"] == "Python"


@pytest.mark.asyncio
async def test_interviewer_topics_covered_grows_over_questions(interviewer_agent, create_message, create_context):
    ctx = create_context()
    msg = create_message(data={"action": "start_interview", "domain": "Python"})
    await interviewer_agent.process(msg, ctx)
    first_topics = list(ctx.get("topics_covered"))

    msg2 = create_message(data={"action": "next_question"})
    await interviewer_agent.process(msg2, ctx)
    assert len(ctx.get("topics_covered")) > len(first_topics)


@pytest.mark.asyncio
async def test_interviewer_resets_when_all_topics_covered(interviewer_agent, create_message, create_context):
    all_topics = list({q["topic"] for q in MOCK_QUESTIONS["Python"]})
    ctx = create_context(shared_state={
        "domain": "Python", "difficulty": "medium",
        "current_question": 6, "total_questions": 10,
        "topics_covered": all_topics,
    })
    msg = create_message(data={"action": "next_question"})
    result = await interviewer_agent.process(msg, ctx)
    # Should still return a valid question even when all topics covered
    assert "question" in result.data


def test_difficulty_map_contains_all_levels():
    assert "easy" in DIFFICULTY_MAP
    assert "medium" in DIFFICULTY_MAP
    assert "hard" in DIFFICULTY_MAP


def test_mock_questions_has_all_domains():
    expected = {"Python", "JavaScript", "React", "iOS", "Android", "ReactNative", "Java", "DevOps", "SystemDesign", "HR"}
    assert set(MOCK_QUESTIONS.keys()) == expected
