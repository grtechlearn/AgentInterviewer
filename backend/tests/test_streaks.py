"""
Tests for Streak Tracking - 14 tests.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from backend.gamification.streaks import (
    update_streak,
    calculate_streak_bonus,
    get_streak_message,
    GRACE_PERIOD_DAYS,
)


# --- update_streak tests ---


def test_update_streak_first_time_user():
    streak, broken, grace = update_streak(None, today=date(2024, 1, 15))
    assert streak == 1
    assert broken is False
    assert grace is False


def test_update_streak_same_day():
    today = date(2024, 1, 15)
    streak, broken, grace = update_streak(today, today=today)
    assert streak == 1
    assert broken is False
    assert grace is False


def test_update_streak_consecutive_day():
    yesterday = date(2024, 1, 14)
    today = date(2024, 1, 15)
    streak, broken, grace = update_streak(yesterday, today=today)
    assert streak == 1
    assert broken is False
    assert grace is False


def test_update_streak_grace_period():
    two_days_ago = date(2024, 1, 13)
    today = date(2024, 1, 15)
    streak, broken, grace = update_streak(two_days_ago, today=today)
    assert streak == 1
    assert broken is False
    assert grace is True


def test_update_streak_broken_3_days():
    three_days_ago = date(2024, 1, 12)
    today = date(2024, 1, 15)
    streak, broken, grace = update_streak(three_days_ago, today=today)
    assert streak == 1
    assert broken is True
    assert grace is False


def test_update_streak_broken_week():
    week_ago = date(2024, 1, 8)
    today = date(2024, 1, 15)
    streak, broken, grace = update_streak(week_ago, today=today)
    assert broken is True


def test_update_streak_none_last_date():
    streak, broken, grace = update_streak(None)
    assert streak == 1
    assert broken is False


# --- calculate_streak_bonus tests ---


def test_streak_bonus_zero():
    assert calculate_streak_bonus(0) == 0
    assert calculate_streak_bonus(1) == 0
    assert calculate_streak_bonus(2) == 0


def test_streak_bonus_3():
    assert calculate_streak_bonus(3) == 10
    assert calculate_streak_bonus(6) == 10


def test_streak_bonus_7():
    assert calculate_streak_bonus(7) == 20
    assert calculate_streak_bonus(13) == 20


def test_streak_bonus_14():
    assert calculate_streak_bonus(14) == 30


def test_streak_bonus_30():
    assert calculate_streak_bonus(30) == 50


def test_streak_bonus_60():
    assert calculate_streak_bonus(60) == 75


def test_streak_bonus_100():
    assert calculate_streak_bonus(100) == 100
    assert calculate_streak_bonus(200) == 100


# --- get_streak_message tests ---


def test_streak_message_zero():
    msg = get_streak_message(0)
    assert "Start practicing" in msg


def test_streak_message_day_1():
    msg = get_streak_message(1)
    assert "Day 1" in msg


def test_streak_message_3():
    msg = get_streak_message(3)
    assert "3-day" in msg


def test_streak_message_7():
    msg = get_streak_message(7)
    assert "week" in msg.lower()


def test_streak_message_14():
    msg = get_streak_message(14)
    assert "14-day" in msg


def test_streak_message_30():
    msg = get_streak_message(30)
    assert "month" in msg.lower()


def test_streak_message_60():
    msg = get_streak_message(60)
    assert "60-day" in msg


def test_streak_message_100():
    msg = get_streak_message(100)
    assert "legend" in msg.lower()


def test_grace_period_constant():
    assert GRACE_PERIOD_DAYS == 1
