"""
Tests for Achievements / Badge System - 13 tests.
"""

from __future__ import annotations

import pytest

from backend.gamification.achievements import (
    check_achievements,
    get_all_achievements,
    ACHIEVEMENT_DEFINITIONS,
)


def test_check_achievements_with_no_stats():
    result = check_achievements({})
    # With all zeros, no achievements should unlock
    assert isinstance(result, list)
    assert len(result) == 0


def test_check_achievements_first_question():
    stats = {"total_answers": 1}
    result = check_achievements(stats)
    ids = [a["id"] for a in result]
    assert "first_question" in ids


def test_check_achievements_ten_answers():
    stats = {"total_answers": 10}
    result = check_achievements(stats)
    ids = [a["id"] for a in result]
    assert "ten_answers" in ids
    assert "first_question" in ids


def test_check_achievements_streak_5():
    stats = {"streak": 5}
    result = check_achievements(stats)
    ids = [a["id"] for a in result]
    assert "five_streak" in ids


def test_check_achievements_streak_7():
    stats = {"streak": 7}
    result = check_achievements(stats)
    ids = [a["id"] for a in result]
    assert "seven_streak" in ids


def test_check_achievements_streak_14():
    stats = {"streak": 14}
    result = check_achievements(stats)
    ids = [a["id"] for a in result]
    assert "fourteen_streak" in ids


def test_check_achievements_streak_30():
    stats = {"streak": 30}
    result = check_achievements(stats)
    ids = [a["id"] for a in result]
    assert "thirty_streak" in ids


def test_check_achievements_score_based():
    stats = {"avg_score": 90}
    result = check_achievements(stats)
    ids = [a["id"] for a in result]
    assert "avg_90" in ids
    assert "avg_80" in ids
    assert "avg_70" in ids


def test_check_achievements_already_unlocked_filtered():
    stats = {"total_answers": 10, "unlocked": ["first_question", "ten_answers"]}
    result = check_achievements(stats)
    ids = [a["id"] for a in result]
    assert "first_question" not in ids
    assert "ten_answers" not in ids


def test_check_achievements_level_based():
    stats = {"level": 10}
    result = check_achievements(stats)
    ids = [a["id"] for a in result]
    assert "level_10" in ids
    assert "level_5" in ids


def test_get_all_achievements_returns_30():
    all_a = get_all_achievements()
    assert len(all_a) == 30


def test_get_all_achievements_format():
    all_a = get_all_achievements()
    for a in all_a:
        assert "id" in a
        assert "name" in a
        assert "description" in a
        assert "icon" in a
        assert "category" in a


def test_get_all_achievements_no_condition_lambda():
    all_a = get_all_achievements()
    for a in all_a:
        assert "condition" not in a
