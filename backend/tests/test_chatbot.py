"""
Tests for ChatBotAgent - 10 tests.
"""

from __future__ import annotations

import json

import pytest

from backend.agents.chatbot import ChatBotAgent, CANNED_RESPONSES, DEFAULT_RESPONSE


@pytest.mark.asyncio
async def test_chatbot_returns_response_for_python(chatbot_agent, create_message, create_context):
    msg = create_message(content="Tell me about python")
    ctx = create_context()
    result = await chatbot_agent.process(msg, ctx)
    assert "Python" in result.data["response"]


@pytest.mark.asyncio
async def test_chatbot_returns_response_for_react(chatbot_agent, create_message, create_context):
    msg = create_message(content="What is react?")
    ctx = create_context()
    result = await chatbot_agent.process(msg, ctx)
    assert "React" in result.data["response"]


@pytest.mark.asyncio
async def test_chatbot_returns_response_for_interview(chatbot_agent, create_message, create_context):
    msg = create_message(content="How do I prepare for an interview?")
    ctx = create_context()
    result = await chatbot_agent.process(msg, ctx)
    assert "interview" in result.data["response"].lower()


@pytest.mark.asyncio
async def test_chatbot_returns_response_for_system_design(chatbot_agent, create_message, create_context):
    msg = create_message(content="Tell me about system design")
    ctx = create_context()
    result = await chatbot_agent.process(msg, ctx)
    assert "design" in result.data["response"].lower()


@pytest.mark.asyncio
async def test_chatbot_handles_empty_message(chatbot_agent, create_message, create_context):
    msg = create_message(content="")
    ctx = create_context()
    result = await chatbot_agent.process(msg, ctx)
    assert result.data["response"] == DEFAULT_RESPONSE


@pytest.mark.asyncio
async def test_chatbot_handles_unknown_topic(chatbot_agent, create_message, create_context):
    msg = create_message(content="xyzzyplugh")
    ctx = create_context()
    result = await chatbot_agent.process(msg, ctx)
    assert result.data["response"] == DEFAULT_RESPONSE


@pytest.mark.asyncio
async def test_chatbot_mock_mode_flag(chatbot_agent, create_message, create_context):
    msg = create_message(content="python")
    ctx = create_context()
    result = await chatbot_agent.process(msg, ctx)
    assert result.data["mock_mode"] is True


@pytest.mark.asyncio
async def test_chatbot_suggestion_present(chatbot_agent, create_message, create_context):
    msg = create_message(content="hello")
    ctx = create_context()
    result = await chatbot_agent.process(msg, ctx)
    assert "suggestion" in result.data


@pytest.mark.asyncio
async def test_chatbot_content_is_valid_json(chatbot_agent, create_message, create_context):
    msg = create_message(content="python")
    ctx = create_context()
    result = await chatbot_agent.process(msg, ctx)
    parsed = json.loads(result.content)
    assert "response" in parsed


@pytest.mark.asyncio
async def test_chatbot_career_keyword(chatbot_agent, create_message, create_context):
    msg = create_message(content="How to grow my career?")
    ctx = create_context()
    result = await chatbot_agent.process(msg, ctx)
    assert "career" in result.data["response"].lower() or "Build" in result.data["response"]
