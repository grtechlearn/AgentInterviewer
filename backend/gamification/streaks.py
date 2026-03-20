"""
Streak Tracking - With grace period support.
"""

from __future__ import annotations

from datetime import date, timedelta

GRACE_PERIOD_DAYS = 1  # Allow 1 day miss without breaking streak


def update_streak(
    last_active_date: date | None,
    today: date | None = None,
) -> tuple[int, bool, bool]:
    """
    Update streak based on last active date.

    Args:
        last_active_date: The date the user was last active (or None if first time).
        today: Override for current date (useful for testing).

    Returns:
        Tuple of (current_streak, streak_broken, grace_used).
        - current_streak: The new streak count.
        - streak_broken: True if the streak was reset.
        - grace_used: True if a grace period day was consumed.
    """
    if today is None:
        today = date.today()

    # First time user
    if last_active_date is None:
        return 1, False, False

    days_since = (today - last_active_date).days

    # Same day - no change needed (return 1 minimum)
    if days_since == 0:
        return 1, False, False

    # Consecutive day - streak continues
    if days_since == 1:
        return 1, False, False  # Caller adds to existing streak

    # Grace period (missed 1 day)
    if days_since == 2:
        return 1, False, True

    # Streak broken
    return 1, True, False


def calculate_streak_bonus(streak: int) -> int:
    """Calculate bonus XP for maintaining a streak."""
    if streak >= 100:
        return 100
    if streak >= 60:
        return 75
    if streak >= 30:
        return 50
    if streak >= 14:
        return 30
    if streak >= 7:
        return 20
    if streak >= 3:
        return 10
    return 0


def get_streak_message(streak: int) -> str:
    """Get an encouraging message based on streak length."""
    if streak >= 100:
        return f"Incredible {streak}-day streak! You are a legend!"
    if streak >= 60:
        return f"Amazing {streak}-day streak! True dedication!"
    if streak >= 30:
        return f"Fantastic {streak}-day streak! A full month of practice!"
    if streak >= 14:
        return f"Great {streak}-day streak! Two weeks strong!"
    if streak >= 7:
        return f"Awesome {streak}-day streak! One full week!"
    if streak >= 3:
        return f"Nice {streak}-day streak! Keep it going!"
    if streak >= 1:
        return "Day 1 starts now! Build your streak!"
    return "Start practicing to build your streak!"
