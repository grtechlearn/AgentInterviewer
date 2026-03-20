"""
Tests for ResumeAnalyzerAgent - 10 tests.
"""

from __future__ import annotations

import json

import pytest

from backend.agents.resume_analyzer import ResumeAnalyzerAgent, SKILL_KEYWORDS, TAILORED_QUESTIONS


@pytest.mark.asyncio
async def test_analyze_detects_python_skills(resume_analyzer_agent, create_message, create_context):
    msg = create_message(data={"action": "analyze_resume", "resume_text": "Experienced Python developer with Django and Flask expertise."})
    ctx = create_context()
    result = await resume_analyzer_agent.process(msg, ctx)
    assert "Python" in result.data["suggested_domains"]


@pytest.mark.asyncio
async def test_analyze_detects_multiple_domains(resume_analyzer_agent, create_message, create_context):
    msg = create_message(data={"action": "analyze_resume", "resume_text": "Full stack developer: Python, React, Docker, Kubernetes."})
    ctx = create_context()
    result = await resume_analyzer_agent.process(msg, ctx)
    domains = result.data["suggested_domains"]
    assert "Python" in domains
    assert "React" in domains
    assert "DevOps" in domains


@pytest.mark.asyncio
async def test_analyze_detects_senior_by_years(resume_analyzer_agent, create_message, create_context):
    msg = create_message(data={"action": "analyze_resume", "resume_text": "Software engineer with 8 years experience in Java and Spring."})
    ctx = create_context()
    result = await resume_analyzer_agent.process(msg, ctx)
    assert result.data["experience_level"] == "senior"
    assert result.data["years_detected"] == 8


@pytest.mark.asyncio
async def test_analyze_detects_junior_by_keyword(resume_analyzer_agent, create_message, create_context):
    msg = create_message(data={"action": "analyze_resume", "resume_text": "Recent graduate and fresher looking for entry level Python role."})
    ctx = create_context()
    result = await resume_analyzer_agent.process(msg, ctx)
    assert result.data["experience_level"] == "junior"


@pytest.mark.asyncio
async def test_analyze_stores_in_context(resume_analyzer_agent, create_message, create_context):
    msg = create_message(data={"action": "analyze_resume", "resume_text": "Python developer with React experience."})
    ctx = create_context()
    await resume_analyzer_agent.process(msg, ctx)
    assert ctx.get("extracted_skills") is not None
    assert ctx.get("suggested_domains") is not None
    assert ctx.get("experience_level") is not None


@pytest.mark.asyncio
async def test_analyze_empty_resume_falls_back(resume_analyzer_agent, create_message, create_context):
    msg = create_message(data={"action": "analyze_resume", "resume_text": ""})
    ctx = create_context()
    result = await resume_analyzer_agent.process(msg, ctx)
    assert result.data["suggested_domains"] == ["Python"]
    assert result.data["experience_level"] == "junior"


@pytest.mark.asyncio
async def test_get_tailored_questions_after_analyze(resume_analyzer_agent, create_message, create_context):
    ctx = create_context()
    msg1 = create_message(data={"action": "analyze_resume", "resume_text": "Python developer with Django."})
    await resume_analyzer_agent.process(msg1, ctx)
    msg2 = create_message(data={"action": "get_tailored_questions"})
    result = await resume_analyzer_agent.process(msg2, ctx)
    assert len(result.data["tailored_questions"]) > 0
    assert "Python" in result.data["based_on_domains"]


@pytest.mark.asyncio
async def test_get_tailored_questions_default_when_no_domains(resume_analyzer_agent, create_message, create_context):
    msg = create_message(data={"action": "get_tailored_questions"})
    ctx = create_context()
    result = await resume_analyzer_agent.process(msg, ctx)
    assert result.data["tailored_questions"] == TAILORED_QUESTIONS["default"]


@pytest.mark.asyncio
async def test_content_is_valid_json(resume_analyzer_agent, create_message, create_context):
    msg = create_message(data={"action": "analyze_resume", "resume_text": "React developer."})
    ctx = create_context()
    result = await resume_analyzer_agent.process(msg, ctx)
    parsed = json.loads(result.content)
    assert "extracted_skills" in parsed


@pytest.mark.asyncio
async def test_unknown_action_returns_error(resume_analyzer_agent, create_message, create_context):
    msg = create_message(data={"action": "rewrite_resume"})
    ctx = create_context()
    result = await resume_analyzer_agent.process(msg, ctx)
    assert "Unknown action" in result.content
