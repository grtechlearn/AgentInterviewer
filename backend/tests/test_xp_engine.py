"""
Tests for XP Engine - 18 tests.
"""

from __future__ import annotations

import pytest

from backend.gamification.xp_engine import (
    calculate_xp,
    get_level,
    get_level_progress,
    XP_TABLE,
    LEVELS,
)


# --- calculate_xp tests ---


def test_calculate_xp_answer_question_no_score():
    xp = calculate_xp("answer_question")
    assert xp == XP_TABLE["answer_question"]


def test_calculate_xp_answer_question_with_score():
    xp = calculate_xp("answer_question", score=80)
    # base=10, multiplier=0.8, int(10 * (0.5 + 0.8)) = 13
    assert xp == 13


def test_calculate_xp_answer_question_perfect_score():
    xp = calculate_xp("answer_question", score=100)
    # base=10, multiplier=1.0, int(10 * 1.5) = 15, +50 perfect bonus = 65
    assert xp == 65


def test_calculate_xp_answer_question_95_gets_perfect_bonus():
    xp = calculate_xp("answer_question", score=95)
    # base=10, multiplier=0.95, int(10 * 1.45) = 14, +50 = 64
    assert xp == 64


def test_calculate_xp_correct_answer_with_score():
    xp = calculate_xp("correct_answer", score=50)
    # base=20, multiplier=0.5, int(20 * 1.0) = 20
    assert xp == 20


def test_calculate_xp_complete_session():
    xp = calculate_xp("complete_session")
    assert xp == XP_TABLE["complete_session"]


def test_calculate_xp_daily_streak():
    xp = calculate_xp("daily_streak")
    assert xp == XP_TABLE["daily_streak"]


def test_calculate_xp_quiz_perfect():
    xp = calculate_xp("quiz_perfect")
    assert xp == XP_TABLE["quiz_perfect"]


def test_calculate_xp_unknown_action():
    xp = calculate_xp("totally_unknown")
    assert xp == 5  # default


def test_calculate_xp_minimum_is_1():
    # Even with weird inputs, minimum XP should be 1
    xp = calculate_xp("answer_question", score=0)
    assert xp >= 1


# --- get_level tests ---


def test_get_level_zero_xp():
    level, title, xp_next = get_level(0)
    assert level == 1
    assert title == "Apprentice I"
    assert xp_next == 100


def test_get_level_100_xp():
    level, title, xp_next = get_level(100)
    assert level == 2
    assert title == "Apprentice II"


def test_get_level_1000_xp():
    level, title, _ = get_level(1000)
    assert level == 6
    assert title == "Developer I"


def test_get_level_max_xp():
    level, title, xp_next = get_level(200000)
    assert level == 30
    assert title == "Legend V"
    assert xp_next == 0  # Max level


def test_get_level_mid_range():
    level, title, _ = get_level(5000)
    assert level == 12
    assert title == "Senior II"


# --- get_level_progress tests ---


def test_get_level_progress_zero():
    progress = get_level_progress(0)
    assert progress["level"] == 1
    assert progress["total_xp"] == 0
    assert progress["xp_to_next"] == 100
    assert progress["progress_pct"] == 0


def test_get_level_progress_mid_level():
    progress = get_level_progress(150)
    assert progress["level"] == 2
    assert progress["title"] == "Apprentice II"
    assert 0 <= progress["progress_pct"] <= 100


def test_get_level_progress_max_level():
    progress = get_level_progress(200000)
    assert progress["level"] == 30
    assert progress["progress_pct"] == 100
