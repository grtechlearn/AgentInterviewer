"""
Tests for ForumPostingAgent - 10 tests.
"""

from __future__ import annotations

import json

import pytest

from backend.agents.forum_posting import ForumPostingAgent, DAILY_CHALLENGES, DISCUSSION_TOPICS


@pytest.mark.asyncio
async def test_daily_challenge_returns_challenge(forum_posting_agent, create_message, create_context):
    msg = create_message(data={"action": "daily_challenge"})
    ctx = create_context()
    result = await forum_posting_agent.process(msg, ctx)
    assert "title" in result.data
    assert "content" in result.data
    assert "difficulty" in result.data
    assert "engagement_hook" in result.data


@pytest.mark.asyncio
async def test_daily_challenge_filtered_by_domain(forum_posting_agent, create_message, create_context):
    msg = create_message(data={"action": "daily_challenge", "domain": "Python"})
    ctx = create_context()
    result = await forum_posting_agent.process(msg, ctx)
    assert result.data["domain"] == "Python"


@pytest.mark.asyncio
async def test_daily_challenge_unknown_domain_falls_back(forum_posting_agent, create_message, create_context):
    msg = create_message(data={"action": "daily_challenge", "domain": "Haskell"})
    ctx = create_context()
    result = await forum_posting_agent.process(msg, ctx)
    # Falls back to any challenge
    assert "title" in result.data


@pytest.mark.asyncio
async def test_topic_discussion_returns_topic(forum_posting_agent, create_message, create_context):
    msg = create_message(data={"action": "topic_discussion"})
    ctx = create_context()
    result = await forum_posting_agent.process(msg, ctx)
    assert "title" in result.data
    assert "content" in result.data
    assert result.data["engagement_hook"] is not None


@pytest.mark.asyncio
async def test_weekly_summary_returns_stats(forum_posting_agent, create_message, create_context):
    msg = create_message(data={"action": "weekly_summary"})
    ctx = create_context()
    result = await forum_posting_agent.process(msg, ctx)
    assert "stats" in result.data
    assert result.data["stats"]["interviews"] == 245
    assert result.data["title"] == "Weekly Community Roundup"


@pytest.mark.asyncio
async def test_social_post_twitter(forum_posting_agent, create_message, create_context):
    msg = create_message(data={"action": "social_post", "platform": "twitter", "domain": "React"})
    ctx = create_context()
    result = await forum_posting_agent.process(msg, ctx)
    assert result.data["platform"] == "twitter"
    assert result.data["domain"] == "React"


@pytest.mark.asyncio
async def test_social_post_linkedin(forum_posting_agent, create_message, create_context):
    msg = create_message(data={"action": "social_post", "platform": "linkedin"})
    ctx = create_context()
    result = await forum_posting_agent.process(msg, ctx)
    assert result.data["platform"] == "linkedin"


@pytest.mark.asyncio
async def test_social_post_content_not_empty(forum_posting_agent, create_message, create_context):
    msg = create_message(data={"action": "social_post"})
    ctx = create_context()
    result = await forum_posting_agent.process(msg, ctx)
    assert len(result.data["content"]) > 0


@pytest.mark.asyncio
async def test_content_is_valid_json(forum_posting_agent, create_message, create_context):
    msg = create_message(data={"action": "weekly_summary"})
    ctx = create_context()
    result = await forum_posting_agent.process(msg, ctx)
    parsed = json.loads(result.content)
    assert "title" in parsed


@pytest.mark.asyncio
async def test_unknown_action_returns_error(forum_posting_agent, create_message, create_context):
    msg = create_message(data={"action": "spam_forum"})
    ctx = create_context()
    result = await forum_posting_agent.process(msg, ctx)
    assert "Unknown action" in result.content
