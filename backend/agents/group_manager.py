"""
GroupManagerAgent - Manage study groups for collaborative interview prep.
"""

from __future__ import annotations

import json
from typing import Any

from agentx.core.agent import BaseAgent, AgentConfig
from agentx.core.context import AgentContext
from agentx.core.message import AgentMessage


class GroupManagerAgent(BaseAgent):
    """Manage study groups with in-memory storage via context."""

    def __init__(self, **kwargs: Any):
        config = AgentConfig(
            name="group_manager",
            role="Study Group Manager",
            system_prompt=(
                "You manage study groups for interview preparation. "
                "Create groups, add members, track stats, and manage tasks."
            ),
        )
        super().__init__(config=config, **kwargs)

    async def process(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        action = message.data.get("action", "get_group_stats")

        if action == "create_group":
            return self._create_group(message, context)
        if action == "add_member":
            return self._add_member(message, context)
        if action == "get_group_stats":
            return self._get_stats(message, context)
        if action == "set_group_task":
            return self._set_task(message, context)
        if action == "get_leaderboard":
            return self._get_leaderboard(message, context)

        return message.error(f"Unknown action: {action}")

    def _get_groups(self, context: AgentContext) -> dict[str, Any]:
        return context.get("groups", {})

    def _save_groups(self, context: AgentContext, groups: dict[str, Any]) -> None:
        context.set("groups", groups)

    def _create_group(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        name = message.data.get("group_name", "Study Group")
        domain = message.data.get("domain", "Python")
        groups = self._get_groups(context)

        if name in groups:
            return message.error(f"Group '{name}' already exists.")

        groups[name] = {
            "name": name,
            "domain": domain,
            "members": [],
            "current_task": None,
            "interviews_completed": 0,
        }
        self._save_groups(context, groups)
        result = {"group": groups[name], "message": f"Group '{name}' created for {domain}.", "mock_mode": True}
        return message.reply(content=json.dumps(result), data=result)

    def _add_member(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        group_name = message.data.get("group_name", "")
        member = message.data.get("member_name", "")
        groups = self._get_groups(context)

        if group_name not in groups:
            return message.error(f"Group '{group_name}' not found.")
        if member in groups[group_name]["members"]:
            return message.error(f"'{member}' is already in group '{group_name}'.")

        groups[group_name]["members"].append(member)
        self._save_groups(context, groups)
        result = {
            "group_name": group_name,
            "member_added": member,
            "total_members": len(groups[group_name]["members"]),
            "mock_mode": True,
        }
        return message.reply(content=json.dumps(result), data=result)

    def _get_stats(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        group_name = message.data.get("group_name", "")
        groups = self._get_groups(context)

        if group_name not in groups:
            return message.error(f"Group '{group_name}' not found.")

        group = groups[group_name]
        result = {
            "group_name": group["name"],
            "domain": group["domain"],
            "member_count": len(group["members"]),
            "members": group["members"],
            "current_task": group["current_task"],
            "interviews_completed": group["interviews_completed"],
            "mock_mode": True,
        }
        return message.reply(content=json.dumps(result), data=result)

    def _set_task(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        group_name = message.data.get("group_name", "")
        task = message.data.get("task", "Complete 3 mock interviews")
        groups = self._get_groups(context)

        if group_name not in groups:
            return message.error(f"Group '{group_name}' not found.")

        groups[group_name]["current_task"] = task
        self._save_groups(context, groups)
        result = {"group_name": group_name, "task_set": task, "mock_mode": True}
        return message.reply(content=json.dumps(result), data=result)

    def _get_leaderboard(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        group_name = message.data.get("group_name", "")
        groups = self._get_groups(context)

        if group_name not in groups:
            return message.error(f"Group '{group_name}' not found.")

        members = groups[group_name]["members"]
        leaderboard = [
            {"rank": i + 1, "name": m, "score": max(100 - i * 12, 30), "interviews": max(5 - i, 1)}
            for i, m in enumerate(members)
        ]
        result = {
            "group_name": group_name,
            "leaderboard": leaderboard,
            "total_members": len(members),
            "mock_mode": True,
        }
        return message.reply(content=json.dumps(result), data=result)
