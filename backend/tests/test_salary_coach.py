"""
Tests for SalaryCoachAgent - 10 tests.
"""

from __future__ import annotations

import json

import pytest

from backend.agents.salary_coach import SalaryCoachAgent, MOCK_OFFERS, NEGOTIATION_TIPS


@pytest.mark.asyncio
async def test_start_negotiation_returns_offer(salary_coach_agent, create_message, create_context):
    msg = create_message(data={"action": "start_negotiation"})
    ctx = create_context()
    result = await salary_coach_agent.process(msg, ctx)
    assert "offer_amount" in result.data
    assert "company" in result.data
    assert "role" in result.data
    assert result.data["mock_mode"] is True


@pytest.mark.asyncio
async def test_start_negotiation_stores_offer_in_context(salary_coach_agent, create_message, create_context):
    msg = create_message(data={"action": "start_negotiation"})
    ctx = create_context()
    await salary_coach_agent.process(msg, ctx)
    assert ctx.get("current_offer") is not None
    assert ctx.get("negotiation_round") == 1


@pytest.mark.asyncio
async def test_respond_confident_strategy(salary_coach_agent, create_message, create_context):
    offer = MOCK_OFFERS[0]
    ctx = create_context(shared_state={"current_offer": offer, "negotiation_round": 1})
    msg = create_message(data={"action": "respond", "response": "Based on my research and market data, I believe..."})
    result = await salary_coach_agent.process(msg, ctx)
    assert result.data["strategy_detected"] == "confident"
    assert result.data["rating"] == 9


@pytest.mark.asyncio
async def test_respond_aggressive_strategy(salary_coach_agent, create_message, create_context):
    offer = MOCK_OFFERS[0]
    ctx = create_context(shared_state={"current_offer": offer, "negotiation_round": 1})
    msg = create_message(data={"action": "respond", "response": "I demand at least double or else I walk."})
    result = await salary_coach_agent.process(msg, ctx)
    assert result.data["strategy_detected"] == "aggressive"
    assert result.data["rating"] == 5


@pytest.mark.asyncio
async def test_respond_passive_strategy(salary_coach_agent, create_message, create_context):
    offer = MOCK_OFFERS[0]
    ctx = create_context(shared_state={"current_offer": offer, "negotiation_round": 1})
    msg = create_message(data={"action": "respond", "response": "That sounds fine, I accept."})
    result = await salary_coach_agent.process(msg, ctx)
    assert result.data["strategy_detected"] == "passive"


@pytest.mark.asyncio
async def test_respond_reasonable_strategy(salary_coach_agent, create_message, create_context):
    offer = MOCK_OFFERS[0]
    ctx = create_context(shared_state={"current_offer": offer, "negotiation_round": 1})
    msg = create_message(data={"action": "respond", "response": "I think a fair compensation would consider my experience."})
    result = await salary_coach_agent.process(msg, ctx)
    assert result.data["strategy_detected"] == "reasonable"


@pytest.mark.asyncio
async def test_respond_increments_round(salary_coach_agent, create_message, create_context):
    offer = MOCK_OFFERS[0]
    ctx = create_context(shared_state={"current_offer": offer, "negotiation_round": 1})
    msg = create_message(data={"action": "respond", "response": "Let me consider this."})
    await salary_coach_agent.process(msg, ctx)
    assert ctx.get("negotiation_round") == 2


@pytest.mark.asyncio
async def test_get_tips_returns_list(salary_coach_agent, create_message, create_context):
    msg = create_message(data={"action": "get_tips", "count": 3})
    ctx = create_context()
    result = await salary_coach_agent.process(msg, ctx)
    assert len(result.data["tips"]) == 3
    assert result.data["total_available"] == len(NEGOTIATION_TIPS)


@pytest.mark.asyncio
async def test_get_tips_default_count(salary_coach_agent, create_message, create_context):
    msg = create_message(data={"action": "get_tips"})
    ctx = create_context()
    result = await salary_coach_agent.process(msg, ctx)
    assert len(result.data["tips"]) == 5


@pytest.mark.asyncio
async def test_unknown_action_returns_error(salary_coach_agent, create_message, create_context):
    msg = create_message(data={"action": "fire_me"})
    ctx = create_context()
    result = await salary_coach_agent.process(msg, ctx)
    assert "Unknown action" in result.content
