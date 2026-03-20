"""
Achievements / Badge System - 30 achievement definitions.
"""

from __future__ import annotations

from typing import Any

ACHIEVEMENT_DEFINITIONS: dict[str, dict[str, Any]] = {
    # Getting started
    "first_question": {"name": "First Step", "description": "Answer your first interview question.", "condition": lambda s: s.get("total_answers", 0) >= 1, "icon": "rocket", "category": "milestone"},
    "first_perfect": {"name": "Flawless", "description": "Score 100 on a question.", "condition": lambda s: s.get("perfect_scores", 0) >= 1, "icon": "star", "category": "skill"},
    "five_streak": {"name": "On Fire", "description": "Maintain a 5-day streak.", "condition": lambda s: s.get("streak", 0) >= 5, "icon": "fire", "category": "streak"},

    # Volume
    "ten_answers": {"name": "Getting Warmed Up", "description": "Answer 10 questions.", "condition": lambda s: s.get("total_answers", 0) >= 10, "icon": "zap", "category": "milestone"},
    "fifty_answers": {"name": "Half Century", "description": "Answer 50 questions.", "condition": lambda s: s.get("total_answers", 0) >= 50, "icon": "medal", "category": "milestone"},
    "hundred_answers": {"name": "Centurion", "description": "Answer 100 questions.", "condition": lambda s: s.get("total_answers", 0) >= 100, "icon": "trophy", "category": "milestone"},
    "five_hundred": {"name": "Marathoner", "description": "Answer 500 questions.", "condition": lambda s: s.get("total_answers", 0) >= 500, "icon": "crown", "category": "milestone"},

    # Streaks
    "seven_streak": {"name": "Week Warrior", "description": "7-day practice streak.", "condition": lambda s: s.get("streak", 0) >= 7, "icon": "calendar", "category": "streak"},
    "fourteen_streak": {"name": "Fortnight Force", "description": "14-day practice streak.", "condition": lambda s: s.get("streak", 0) >= 14, "icon": "calendar", "category": "streak"},
    "thirty_streak": {"name": "Monthly Master", "description": "30-day practice streak.", "condition": lambda s: s.get("streak", 0) >= 30, "icon": "calendar", "category": "streak"},
    "sixty_streak": {"name": "Two-Month Titan", "description": "60-day practice streak.", "condition": lambda s: s.get("streak", 0) >= 60, "icon": "diamond", "category": "streak"},
    "hundred_streak": {"name": "100 Days Strong", "description": "100-day practice streak.", "condition": lambda s: s.get("streak", 0) >= 100, "icon": "crown", "category": "streak"},

    # Scores
    "avg_70": {"name": "Solid Performer", "description": "Maintain 70+ average score.", "condition": lambda s: s.get("avg_score", 0) >= 70, "icon": "thumbsup", "category": "skill"},
    "avg_80": {"name": "Top Performer", "description": "Maintain 80+ average score.", "condition": lambda s: s.get("avg_score", 0) >= 80, "icon": "star", "category": "skill"},
    "avg_90": {"name": "Elite", "description": "Maintain 90+ average score.", "condition": lambda s: s.get("avg_score", 0) >= 90, "icon": "diamond", "category": "skill"},
    "five_perfect": {"name": "Perfectionist", "description": "Score 100 on 5 questions.", "condition": lambda s: s.get("perfect_scores", 0) >= 5, "icon": "star", "category": "skill"},

    # Domains
    "two_domains": {"name": "Explorer", "description": "Practice in 2 different domains.", "condition": lambda s: s.get("domains_practiced", 0) >= 2, "icon": "compass", "category": "breadth"},
    "five_domains": {"name": "Versatile", "description": "Practice in 5 different domains.", "condition": lambda s: s.get("domains_practiced", 0) >= 5, "icon": "globe", "category": "breadth"},
    "all_domains": {"name": "Full Stack", "description": "Practice in all 10 domains.", "condition": lambda s: s.get("domains_practiced", 0) >= 10, "icon": "shield", "category": "breadth"},

    # Quizzes
    "first_quiz": {"name": "Quiz Taker", "description": "Complete your first quiz.", "condition": lambda s: s.get("quizzes_completed", 0) >= 1, "icon": "check", "category": "quiz"},
    "ten_quizzes": {"name": "Quiz Enthusiast", "description": "Complete 10 quizzes.", "condition": lambda s: s.get("quizzes_completed", 0) >= 10, "icon": "check", "category": "quiz"},
    "quiz_perfect": {"name": "Quiz Ace", "description": "Get a perfect quiz score.", "condition": lambda s: s.get("perfect_quizzes", 0) >= 1, "icon": "star", "category": "quiz"},

    # Sessions
    "first_session": {"name": "Interview Ready", "description": "Complete a full interview session.", "condition": lambda s: s.get("sessions_completed", 0) >= 1, "icon": "briefcase", "category": "milestone"},
    "ten_sessions": {"name": "Seasoned", "description": "Complete 10 interview sessions.", "condition": lambda s: s.get("sessions_completed", 0) >= 10, "icon": "briefcase", "category": "milestone"},

    # XP / Level
    "level_5": {"name": "Rising Star", "description": "Reach Level 5.", "condition": lambda s: s.get("level", 1) >= 5, "icon": "trending", "category": "level"},
    "level_10": {"name": "Developer", "description": "Reach Level 10.", "condition": lambda s: s.get("level", 1) >= 10, "icon": "trending", "category": "level"},
    "level_15": {"name": "Senior Dev", "description": "Reach Level 15.", "condition": lambda s: s.get("level", 1) >= 15, "icon": "trending", "category": "level"},
    "level_20": {"name": "Expert", "description": "Reach Level 20.", "condition": lambda s: s.get("level", 1) >= 20, "icon": "trending", "category": "level"},
    "level_25": {"name": "Master", "description": "Reach Level 25.", "condition": lambda s: s.get("level", 1) >= 25, "icon": "crown", "category": "level"},

    # Special
    "night_owl": {"name": "Night Owl", "description": "Practice after midnight.", "condition": lambda s: s.get("late_night_sessions", 0) >= 1, "icon": "moon", "category": "special"},
}


def check_achievements(user_stats: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Check which achievements are newly unlocked.

    Args:
        user_stats: Dict with keys like total_answers, streak, avg_score,
                    domains_practiced, level, etc.
                    Should also include 'unlocked' list of already-unlocked IDs.

    Returns:
        List of newly unlocked achievement dicts.
    """
    already_unlocked = set(user_stats.get("unlocked", []))
    newly_unlocked = []

    for aid, defn in ACHIEVEMENT_DEFINITIONS.items():
        if aid in already_unlocked:
            continue
        try:
            if defn["condition"](user_stats):
                newly_unlocked.append({
                    "id": aid,
                    "name": defn["name"],
                    "description": defn["description"],
                    "icon": defn["icon"],
                    "category": defn["category"],
                })
        except Exception:
            continue

    return newly_unlocked


def get_all_achievements() -> list[dict[str, str]]:
    """Return all achievement definitions (without condition lambdas)."""
    return [
        {
            "id": aid,
            "name": d["name"],
            "description": d["description"],
            "icon": d["icon"],
            "category": d["category"],
        }
        for aid, d in ACHIEVEMENT_DEFINITIONS.items()
    ]
