"""
Tests for AdminAnalyticsAgent - 10 tests.
"""

from __future__ import annotations

import json

import pytest

from backend.agents.admin_analytics import AdminAnalyticsAgent


@pytest.mark.asyncio
async def test_system_overview_returns_stats(admin_analytics_agent, create_message, create_context):
    msg = create_message(data={"action": "system_overview"})
    ctx = create_context()
    result = await admin_analytics_agent.process(msg, ctx)
    assert result.data["total_users"] == 1247
    assert result.data["active_users"] == 389
    assert result.data["interviews_today"] == 156


@pytest.mark.asyncio
async def test_system_overview_has_top_domains(admin_analytics_agent, create_message, create_context):
    msg = create_message(data={"action": "system_overview"})
    ctx = create_context()
    result = await admin_analytics_agent.process(msg, ctx)
    assert len(result.data["top_domains"]) == 3
    assert result.data["system_uptime_pct"] == 99.7


@pytest.mark.asyncio
async def test_user_report_default_period(admin_analytics_agent, create_message, create_context):
    msg = create_message(data={"action": "user_report"})
    ctx = create_context()
    result = await admin_analytics_agent.process(msg, ctx)
    assert result.data["period"] == "weekly"
    assert result.data["new_signups"] == 87
    assert result.data["retention_rate_pct"] == 82.3


@pytest.mark.asyncio
async def test_user_report_custom_period(admin_analytics_agent, create_message, create_context):
    msg = create_message(data={"action": "user_report", "period": "monthly"})
    ctx = create_context()
    result = await admin_analytics_agent.process(msg, ctx)
    assert result.data["period"] == "monthly"


@pytest.mark.asyncio
async def test_user_report_has_domain_breakdown(admin_analytics_agent, create_message, create_context):
    msg = create_message(data={"action": "user_report"})
    ctx = create_context()
    result = await admin_analytics_agent.process(msg, ctx)
    assert len(result.data["top_user_domains"]) == 3
    assert result.data["top_user_domains"][0]["domain"] == "Python"


@pytest.mark.asyncio
async def test_agent_performance_returns_agents(admin_analytics_agent, create_message, create_context):
    msg = create_message(data={"action": "agent_performance"})
    ctx = create_context()
    result = await admin_analytics_agent.process(msg, ctx)
    assert len(result.data["agents"]) >= 5
    assert result.data["total_requests"] > 0


@pytest.mark.asyncio
async def test_agent_performance_has_latency(admin_analytics_agent, create_message, create_context):
    msg = create_message(data={"action": "agent_performance"})
    ctx = create_context()
    result = await admin_analytics_agent.process(msg, ctx)
    for agent in result.data["agents"]:
        assert "avg_latency_ms" in agent
        assert "error_rate_pct" in agent


@pytest.mark.asyncio
async def test_cost_report_default_period(admin_analytics_agent, create_message, create_context):
    msg = create_message(data={"action": "cost_report"})
    ctx = create_context()
    result = await admin_analytics_agent.process(msg, ctx)
    assert result.data["period"] == "monthly"
    assert result.data["total_cost_usd"] == 284.50


@pytest.mark.asyncio
async def test_cost_report_has_breakdown(admin_analytics_agent, create_message, create_context):
    msg = create_message(data={"action": "cost_report"})
    ctx = create_context()
    result = await admin_analytics_agent.process(msg, ctx)
    assert len(result.data["cost_breakdown"]) == 4
    total_pct = sum(item["pct"] for item in result.data["cost_breakdown"])
    assert abs(total_pct - 100.0) < 0.1


@pytest.mark.asyncio
async def test_unknown_action_returns_error(admin_analytics_agent, create_message, create_context):
    msg = create_message(data={"action": "delete_everything"})
    ctx = create_context()
    result = await admin_analytics_agent.process(msg, ctx)
    assert "Unknown action" in result.content
