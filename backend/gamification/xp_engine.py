"""
XP Engine - Experience points calculation and level system.
"""

from __future__ import annotations

# XP rewards per action
XP_TABLE: dict[str, int] = {
    "answer_question": 10,
    "correct_answer": 20,
    "perfect_score": 50,
    "complete_session": 30,
    "daily_streak": 15,
    "weekly_streak": 50,
    "first_question": 25,
    "quiz_complete": 20,
    "quiz_perfect": 75,
    "achievement_unlock": 10,
}

# Level thresholds and titles
LEVELS = [
    (1, "Apprentice I", 0),
    (2, "Apprentice II", 100),
    (3, "Apprentice III", 250),
    (4, "Apprentice IV", 450),
    (5, "Apprentice V", 700),
    (6, "Developer I", 1000),
    (7, "Developer II", 1400),
    (8, "Developer III", 1900),
    (9, "Developer IV", 2500),
    (10, "Developer V", 3200),
    (11, "Senior I", 4000),
    (12, "Senior II", 5000),
    (13, "Senior III", 6200),
    (14, "Senior IV", 7600),
    (15, "Senior V", 9200),
    (16, "Expert I", 11000),
    (17, "Expert II", 13000),
    (18, "Expert III", 15500),
    (19, "Expert IV", 18500),
    (20, "Expert V", 22000),
    (21, "Master I", 26000),
    (22, "Master II", 31000),
    (23, "Master III", 37000),
    (24, "Master IV", 44000),
    (25, "Master V", 52000),
    (26, "Legend I", 62000),
    (27, "Legend II", 74000),
    (28, "Legend III", 88000),
    (29, "Legend IV", 105000),
    (30, "Legend V", 125000),
]


def calculate_xp(action: str, score: int = 0) -> int:
    """
    Calculate XP earned for a given action.

    Args:
        action: The action type (see XP_TABLE).
        score: Optional score (0-100) for score-based bonuses.

    Returns:
        XP amount earned.
    """
    base = XP_TABLE.get(action, 5)

    # Score-based multiplier for answer actions
    if action in ("answer_question", "correct_answer") and score > 0:
        multiplier = score / 100.0
        base = int(base * (0.5 + multiplier))

    # Perfect score bonus
    if score >= 95 and action == "answer_question":
        base += XP_TABLE.get("perfect_score", 50)

    return max(1, base)


def get_level(total_xp: int) -> tuple[int, str, int]:
    """
    Determine level from total XP.

    Args:
        total_xp: Total accumulated XP.

    Returns:
        Tuple of (level_number, title, xp_to_next_level).
    """
    current_level = 1
    current_title = "Apprentice I"
    xp_for_next = LEVELS[1][2] if len(LEVELS) > 1 else 999999

    for i, (level, title, threshold) in enumerate(LEVELS):
        if total_xp >= threshold:
            current_level = level
            current_title = title
            if i + 1 < len(LEVELS):
                xp_for_next = LEVELS[i + 1][2] - total_xp
            else:
                xp_for_next = 0  # Max level
        else:
            break

    return current_level, current_title, max(0, xp_for_next)


def get_level_progress(total_xp: int) -> dict:
    """Get detailed level progress info."""
    level, title, xp_to_next = get_level(total_xp)

    # Find current and next thresholds
    current_threshold = 0
    next_threshold = 0
    for i, (lv, _, threshold) in enumerate(LEVELS):
        if lv == level:
            current_threshold = threshold
            if i + 1 < len(LEVELS):
                next_threshold = LEVELS[i + 1][2]
            else:
                next_threshold = threshold
            break

    range_xp = max(1, next_threshold - current_threshold)
    progress_xp = total_xp - current_threshold
    progress_pct = min(100, round(progress_xp / range_xp * 100))

    return {
        "level": level,
        "title": title,
        "total_xp": total_xp,
        "xp_to_next": xp_to_next,
        "progress_pct": progress_pct,
    }
