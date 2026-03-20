"""
AgentInterviewer - Main entry point.

Starts the AgentX daemon with all interview agents registered,
routing rules configured, and scheduled jobs running.

Usage:
    python app.py
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys

# Add agentx to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "agentx"))

from agentx.app import AgentXApp
from agentx.core.message import AgentMessage
from agentx.core.context import AgentContext
from agentx.daemon.runner import AgentXDaemon

from config import get_app_config, get_daemon_config
from agents.interviewer import InterviewerAgent
from agents.evaluator import EvaluatorAgent
from agents.coach import CoachAgent
from agents.report import ReportAgent
from agents.goal_tracker import GoalTrackerAgent
from agents.motivator import MotivatorAgent
from agents.skill_monitor import SkillMonitorAgent
from agents.quiz_master import QuizMasterAgent
from agents.chatbot import ChatBotAgent
from agents.salary_coach import SalaryCoachAgent
from agents.resume_analyzer import ResumeAnalyzerAgent
from agents.forum_posting import ForumPostingAgent
from agents.group_manager import GroupManagerAgent
from agents.admin_analytics import AdminAnalyticsAgent

logger = logging.getLogger("agentx")


# ------------------------------------------------------------------
# Routing conditions
# ------------------------------------------------------------------

def _route_interviewer(msg: AgentMessage, ctx: AgentContext) -> bool:
    action = msg.data.get("action", "")
    return action in ("start_interview", "next_question", "follow_up")


def _route_evaluator(msg: AgentMessage, ctx: AgentContext) -> bool:
    return msg.data.get("action") == "evaluate" or (
        "answer" in msg.data and "question" in msg.data
    )


def _route_coach(msg: AgentMessage, ctx: AgentContext) -> bool:
    return msg.data.get("action") == "coach"


def _route_report(msg: AgentMessage, ctx: AgentContext) -> bool:
    return msg.data.get("action") == "report"


def _route_goal_tracker(msg: AgentMessage, ctx: AgentContext) -> bool:
    action = msg.data.get("action", "")
    return action in ("set_goal", "get_progress", "update_streak", "check_daily")


def _route_motivator(msg: AgentMessage, ctx: AgentContext) -> bool:
    action = msg.data.get("action", "")
    return action in ("daily_message", "topic_of_day", "celebrate_milestone")


def _route_skill_monitor(msg: AgentMessage, ctx: AgentContext) -> bool:
    action = msg.data.get("action", "")
    return action in ("update_skill", "get_skills", "get_weak_areas")


def _route_quiz_master(msg: AgentMessage, ctx: AgentContext) -> bool:
    action = msg.data.get("action", "")
    return action in ("start_quiz", "submit_answer", "get_results")


def _route_salary_coach(msg: AgentMessage, ctx: AgentContext) -> bool:
    action = msg.data.get("action", "")
    return action in ("start_negotiation", "respond", "get_tips")


def _route_resume_analyzer(msg: AgentMessage, ctx: AgentContext) -> bool:
    action = msg.data.get("action", "")
    return action in ("analyze_resume", "get_tailored_questions")


def _route_forum_posting(msg: AgentMessage, ctx: AgentContext) -> bool:
    action = msg.data.get("action", "")
    return action in ("daily_challenge", "topic_discussion", "weekly_summary", "social_post")


def _route_group_manager(msg: AgentMessage, ctx: AgentContext) -> bool:
    action = msg.data.get("action", "")
    return action in ("create_group", "add_member", "get_group_stats", "set_group_task", "get_leaderboard")


def _route_admin_analytics(msg: AgentMessage, ctx: AgentContext) -> bool:
    action = msg.data.get("action", "")
    return action in ("system_overview", "user_report", "agent_performance", "cost_report")


# ------------------------------------------------------------------
# Scheduled jobs
# ------------------------------------------------------------------

async def daily_motivation_job() -> None:
    """Scheduled: log daily motivation (would push to connected clients)."""
    logger.info("[Scheduled] Daily motivation check triggered")


async def health_summary_job() -> None:
    """Scheduled: log a health summary."""
    logger.info("[Scheduled] Health summary check triggered")


# ------------------------------------------------------------------
# Custom API routes
# ------------------------------------------------------------------

async def handle_gamification(payload: dict) -> dict:
    """Custom endpoint for gamification data."""
    from gamification.xp_engine import calculate_xp, get_level_progress
    from gamification.achievements import check_achievements, get_all_achievements
    from gamification.streaks import get_streak_message

    action = payload.get("action", "status")

    if action == "xp":
        xp_action = payload.get("xp_action", "answer_question")
        score = payload.get("score", 50)
        xp = calculate_xp(xp_action, score)
        return {"xp_earned": xp, "action": xp_action}

    if action == "level":
        total_xp = payload.get("total_xp", 0)
        return get_level_progress(total_xp)

    if action == "achievements":
        user_stats = payload.get("user_stats", {})
        new = check_achievements(user_stats)
        return {"newly_unlocked": new}

    if action == "all_achievements":
        return {"achievements": get_all_achievements()}

    if action == "streak_message":
        streak = payload.get("streak", 0)
        return {"message": get_streak_message(streak)}

    return {"error": f"Unknown gamification action: {action}"}


# ------------------------------------------------------------------
# Main setup
# ------------------------------------------------------------------

def build_app() -> tuple[AgentXApp, AgentXDaemon]:
    """Build and configure the full application."""
    app_config = get_app_config()
    daemon_config = get_daemon_config()

    app = AgentXApp(app_config)
    daemon = AgentXDaemon(app=app, config=daemon_config)

    return app, daemon


async def setup_and_run() -> None:
    """Initialize everything and run the daemon."""
    app, daemon = build_app()

    # Start the app to initialize orchestrator
    await app.start()

    orchestrator = app.orchestrator
    assert orchestrator is not None, "Orchestrator failed to initialize"

    # Register all agents
    orchestrator.register_many(
        InterviewerAgent(),
        EvaluatorAgent(),
        CoachAgent(),
        ReportAgent(),
        GoalTrackerAgent(),
        MotivatorAgent(),
        SkillMonitorAgent(),
        QuizMasterAgent(),
        ChatBotAgent(),
        SalaryCoachAgent(),
        ResumeAnalyzerAgent(),
        ForumPostingAgent(),
        GroupManagerAgent(),
        AdminAnalyticsAgent(),
    )

    # Set up routing rules (higher priority = checked first)
    orchestrator.add_route("interviewer", _route_interviewer, priority=10)
    orchestrator.add_route("evaluator", _route_evaluator, priority=10)
    orchestrator.add_route("coach", _route_coach, priority=8)
    orchestrator.add_route("report", _route_report, priority=8)
    orchestrator.add_route("goal_tracker", _route_goal_tracker, priority=7)
    orchestrator.add_route("motivator", _route_motivator, priority=7)
    orchestrator.add_route("skill_monitor", _route_skill_monitor, priority=7)
    orchestrator.add_route("quiz_master", _route_quiz_master, priority=9)
    orchestrator.add_route("salary_coach", _route_salary_coach, priority=7)
    orchestrator.add_route("resume_analyzer", _route_resume_analyzer, priority=8)
    orchestrator.add_route("forum_posting", _route_forum_posting, priority=6)
    orchestrator.add_route("group_manager", _route_group_manager, priority=6)
    orchestrator.add_route("admin_analytics", _route_admin_analytics, priority=5)

    # Fallback to chatbot for unmatched messages
    orchestrator.set_fallback("chatbot")

    # Define pipelines
    orchestrator.add_pipeline(
        "full_evaluation", ["interviewer", "evaluator", "coach"]
    )
    orchestrator.add_pipeline(
        "session_report", ["report"]
    )

    # Schedule recurring jobs
    daemon.every(hours=24, name="daily_motivation", handler=daily_motivation_job)
    daemon.every(hours=1, name="health_summary", handler=health_summary_job)

    # Custom API endpoints
    if daemon.server:
        daemon.server.add_route("/api/v1/gamification", handle_gamification)

    logger.info("AgentInterviewer setup complete")
    logger.info(f"Registered agents: {list(orchestrator.agents.keys())}")
    logger.info(f"Routes configured: {len(orchestrator.routes)}")
    logger.info(f"Pipelines: {list(orchestrator.pipelines.keys())}")

    # Run forever
    await daemon.run_forever()


def main() -> None:
    """CLI entry point."""
    print("=" * 60)
    print("  AgentInterviewer Backend")
    print("  Powered by AgentX Framework")
    print(f"  Port: {os.getenv('AGENTX_PORT', '8081')}")
    print(f"  Mock Mode: {'ON' if not os.getenv('ANTHROPIC_API_KEY') else 'OFF'}")
    print("=" * 60)

    try:
        asyncio.run(setup_and_run())
    except KeyboardInterrupt:
        print("\nShutdown complete.")


if __name__ == "__main__":
    main()
