"""
ForumPostingAgent - Auto-generate forum content for the community.
"""

from __future__ import annotations

import json
import random
from typing import Any

from agentx.core.agent import BaseAgent, AgentConfig
from agentx.core.context import AgentContext
from agentx.core.message import AgentMessage

DAILY_CHALLENGES: list[dict[str, Any]] = [
    {"title": "Reverse a Linked List", "domain": "Data Structures", "difficulty": "medium", "content": "Implement a function to reverse a singly linked list iteratively and recursively."},
    {"title": "Design a Rate Limiter", "domain": "SystemDesign", "difficulty": "hard", "content": "Design a rate limiter that supports multiple strategies: fixed window, sliding window, and token bucket."},
    {"title": "React Custom Hook Challenge", "domain": "React", "difficulty": "medium", "content": "Build a custom React hook that debounces API calls and caches results."},
    {"title": "Python Generator Pipeline", "domain": "Python", "difficulty": "medium", "content": "Create a data processing pipeline using Python generators for memory-efficient CSV processing."},
    {"title": "SQL Query Optimization", "domain": "Databases", "difficulty": "hard", "content": "Given a slow query joining 3 tables with 10M+ rows, optimize it using indexing and query restructuring."},
]

DISCUSSION_TOPICS: list[dict[str, str]] = [
    {"title": "Monorepo vs Polyrepo: What works for your team?", "content": "Share your experience with repository strategies and the trade-offs you have encountered."},
    {"title": "Is TDD worth the overhead?", "content": "Discuss whether test-driven development improves code quality enough to justify the extra time."},
    {"title": "Remote interview tips from both sides", "content": "What makes a remote technical interview successful? Share tips for candidates and interviewers."},
    {"title": "AI in coding interviews: fair or unfair?", "content": "Should candidates use AI tools during interviews? Where do you draw the line?"},
    {"title": "Best resources for system design prep", "content": "Share books, courses, and YouTube channels that helped you prepare for system design rounds."},
]

SOCIAL_TEMPLATES: list[dict[str, str]] = [
    {"platform": "twitter", "content": "Just completed a {domain} mock interview on AgentInterviewer! Scored {score}%. Practice makes perfect."},
    {"platform": "linkedin", "content": "Excited to share that I've been preparing for {domain} interviews using AI-powered practice. The instant feedback is game-changing!"},
    {"platform": "twitter", "content": "Daily coding challenge: {challenge}. Can you solve it in under 20 minutes?"},
]


class ForumPostingAgent(BaseAgent):
    """Auto-generate forum and social media content."""

    def __init__(self, **kwargs: Any):
        config = AgentConfig(
            name="forum_posting",
            role="Community Content Generator",
            system_prompt=(
                "You generate engaging community content including daily "
                "challenges, discussion topics, and social media posts."
            ),
        )
        super().__init__(config=config, **kwargs)

    async def process(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        action = message.data.get("action", "daily_challenge")

        if action == "daily_challenge":
            return self._daily_challenge(message, context)
        if action == "topic_discussion":
            return self._topic_discussion(message, context)
        if action == "weekly_summary":
            return self._weekly_summary(message, context)
        if action == "social_post":
            return self._social_post(message, context)

        return message.error(f"Unknown action: {action}")

    def _daily_challenge(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        domain = message.data.get("domain")
        if domain:
            matches = [c for c in DAILY_CHALLENGES if c["domain"] == domain]
            challenge = random.choice(matches) if matches else random.choice(DAILY_CHALLENGES)
        else:
            challenge = random.choice(DAILY_CHALLENGES)
        result = {**challenge, "engagement_hook": "Drop your solution in the comments!", "mock_mode": True}
        return message.reply(content=json.dumps(result), data=result)

    def _topic_discussion(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        topic = random.choice(DISCUSSION_TOPICS)
        result = {**topic, "domain": "General", "difficulty": "all", "engagement_hook": "What are your thoughts? Share below!", "mock_mode": True}
        return message.reply(content=json.dumps(result), data=result)

    def _weekly_summary(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        result = {
            "title": "Weekly Community Roundup",
            "content": "This week: 245 interviews completed, 89 new members joined, top domain was Python.",
            "domain": "General",
            "difficulty": "all",
            "stats": {"interviews": 245, "new_members": 89, "top_domain": "Python", "avg_score": 72},
            "engagement_hook": "What would you like to see more of next week?",
            "mock_mode": True,
        }
        return message.reply(content=json.dumps(result), data=result)

    def _social_post(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        platform = message.data.get("platform", "twitter")
        domain = message.data.get("domain", "Python")
        templates = [t for t in SOCIAL_TEMPLATES if t["platform"] == platform]
        template = random.choice(templates) if templates else random.choice(SOCIAL_TEMPLATES)
        content = template["content"].format(domain=domain, score=random.randint(60, 95), challenge="Reverse a Linked List")
        result = {"platform": template["platform"], "content": content, "domain": domain, "mock_mode": True}
        return message.reply(content=json.dumps(result), data=result)
