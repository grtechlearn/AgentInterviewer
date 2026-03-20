"""
Tests for GroupManagerAgent - 12 tests.
"""

from __future__ import annotations

import json

import pytest

from backend.agents.group_manager import GroupManagerAgent


@pytest.mark.asyncio
async def test_create_group(group_manager_agent, create_message, create_context):
    msg = create_message(data={"action": "create_group", "group_name": "PyPals", "domain": "Python"})
    ctx = create_context()
    result = await group_manager_agent.process(msg, ctx)
    assert result.data["group"]["name"] == "PyPals"
    assert result.data["group"]["domain"] == "Python"


@pytest.mark.asyncio
async def test_create_duplicate_group_errors(group_manager_agent, create_message, create_context):
    ctx = create_context()
    msg = create_message(data={"action": "create_group", "group_name": "PyPals"})
    await group_manager_agent.process(msg, ctx)
    result = await group_manager_agent.process(msg, ctx)
    assert "already exists" in result.content


@pytest.mark.asyncio
async def test_add_member(group_manager_agent, create_message, create_context):
    ctx = create_context()
    msg1 = create_message(data={"action": "create_group", "group_name": "Team1"})
    await group_manager_agent.process(msg1, ctx)
    msg2 = create_message(data={"action": "add_member", "group_name": "Team1", "member_name": "Alice"})
    result = await group_manager_agent.process(msg2, ctx)
    assert result.data["member_added"] == "Alice"
    assert result.data["total_members"] == 1


@pytest.mark.asyncio
async def test_add_member_to_nonexistent_group(group_manager_agent, create_message, create_context):
    ctx = create_context()
    msg = create_message(data={"action": "add_member", "group_name": "Ghost", "member_name": "Bob"})
    result = await group_manager_agent.process(msg, ctx)
    assert "not found" in result.content


@pytest.mark.asyncio
async def test_add_duplicate_member_errors(group_manager_agent, create_message, create_context):
    ctx = create_context()
    msg1 = create_message(data={"action": "create_group", "group_name": "Team2"})
    await group_manager_agent.process(msg1, ctx)
    msg2 = create_message(data={"action": "add_member", "group_name": "Team2", "member_name": "Alice"})
    await group_manager_agent.process(msg2, ctx)
    result = await group_manager_agent.process(msg2, ctx)
    assert "already in group" in result.content


@pytest.mark.asyncio
async def test_get_group_stats(group_manager_agent, create_message, create_context):
    ctx = create_context()
    msg1 = create_message(data={"action": "create_group", "group_name": "Stats"})
    await group_manager_agent.process(msg1, ctx)
    msg2 = create_message(data={"action": "add_member", "group_name": "Stats", "member_name": "Eve"})
    await group_manager_agent.process(msg2, ctx)
    msg3 = create_message(data={"action": "get_group_stats", "group_name": "Stats"})
    result = await group_manager_agent.process(msg3, ctx)
    assert result.data["member_count"] == 1
    assert "Eve" in result.data["members"]


@pytest.mark.asyncio
async def test_get_stats_nonexistent_group(group_manager_agent, create_message, create_context):
    ctx = create_context()
    msg = create_message(data={"action": "get_group_stats", "group_name": "NoGroup"})
    result = await group_manager_agent.process(msg, ctx)
    assert "not found" in result.content


@pytest.mark.asyncio
async def test_set_group_task(group_manager_agent, create_message, create_context):
    ctx = create_context()
    msg1 = create_message(data={"action": "create_group", "group_name": "TaskTeam"})
    await group_manager_agent.process(msg1, ctx)
    msg2 = create_message(data={"action": "set_group_task", "group_name": "TaskTeam", "task": "Complete 5 interviews"})
    result = await group_manager_agent.process(msg2, ctx)
    assert result.data["task_set"] == "Complete 5 interviews"


@pytest.mark.asyncio
async def test_set_task_nonexistent_group(group_manager_agent, create_message, create_context):
    ctx = create_context()
    msg = create_message(data={"action": "set_group_task", "group_name": "NoTeam", "task": "Do stuff"})
    result = await group_manager_agent.process(msg, ctx)
    assert "not found" in result.content


@pytest.mark.asyncio
async def test_get_leaderboard(group_manager_agent, create_message, create_context):
    ctx = create_context()
    msg1 = create_message(data={"action": "create_group", "group_name": "Leaders"})
    await group_manager_agent.process(msg1, ctx)
    for name in ["Alice", "Bob", "Charlie"]:
        msg = create_message(data={"action": "add_member", "group_name": "Leaders", "member_name": name})
        await group_manager_agent.process(msg, ctx)
    msg2 = create_message(data={"action": "get_leaderboard", "group_name": "Leaders"})
    result = await group_manager_agent.process(msg2, ctx)
    assert len(result.data["leaderboard"]) == 3
    assert result.data["leaderboard"][0]["rank"] == 1
    assert result.data["leaderboard"][0]["score"] > result.data["leaderboard"][2]["score"]


@pytest.mark.asyncio
async def test_leaderboard_nonexistent_group(group_manager_agent, create_message, create_context):
    ctx = create_context()
    msg = create_message(data={"action": "get_leaderboard", "group_name": "NoGroup"})
    result = await group_manager_agent.process(msg, ctx)
    assert "not found" in result.content


@pytest.mark.asyncio
async def test_unknown_action_returns_error(group_manager_agent, create_message, create_context):
    msg = create_message(data={"action": "disband_group"})
    ctx = create_context()
    result = await group_manager_agent.process(msg, ctx)
    assert "Unknown action" in result.content
