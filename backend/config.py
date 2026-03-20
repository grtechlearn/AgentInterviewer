"""
AgentInterviewer - AgentX configuration.
"""

import os

from agentx.config import (
    AgentXConfig,
    DatabaseConfig,
    Environment,
    LLMConfig,
    ContentModerationConfig,
)
from agentx.daemon.runner import DaemonConfig


def get_app_config() -> AgentXConfig:
    """Build the AgentX application config."""
    return AgentXConfig(
        env=Environment.DEVELOPMENT,
        app_name="AgentInterviewer",
        version="1.0.0",
        debug=True,
        database=DatabaseConfig.memory(),
        llm=LLMConfig.single(
            provider="anthropic",
            model=os.getenv("AGENTX_MODEL", "claude-sonnet-4-6"),
            api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        ),
        moderation=ContentModerationConfig.moderate(),
    )


def get_daemon_config() -> DaemonConfig:
    """Build the daemon config."""
    return DaemonConfig(
        server_enabled=True,
        server_host="0.0.0.0",
        server_port=int(os.getenv("AGENTX_PORT", "8081")),
        cors_origins=["*"],
        scheduler_enabled=True,
        watcher_enabled=False,
        mq_enabled=False,
        watchdog_enabled=True,
        log_level=os.getenv("AGENTX_LOG_LEVEL", "INFO"),
    )
