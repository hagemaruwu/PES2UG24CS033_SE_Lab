"""Lab 6: tests for statement (line) coverage of spam_scoring.py."""

import pytest
from spam_scoring import score_message, classify, filter_inbox, inbox_status


@pytest.mark.parametrize("text,known,links,expected", [
    ("hello there", False, 0, 0),
    ("FREE! winner, prize. urgent cash", False, 0, 10),
    ("HELLO", False, 0, 1),
    ("hello", False, 4, 4),
    ("hello", False, 1, 1),
    ("hello", True, 0, 0),
])
def test_message_scores(text, known, links, expected):
    assert score_message(text, known, links) == expected


@pytest.mark.parametrize("score,expected", [
    (1, "clean"), (4, "suspicious"), (8, "spam"),
])
def test_classification(score, expected):
    assert classify(score) == expected


def test_mixed_inbox():
    messages = [
        ("free winner prize urgent", False, 0),
        ("free winner", False, 0),
        ("hello there", False, 0),
    ]
    assert filter_inbox(messages) == {"spam": 1, "suspicious": 1, "clean": 1}


@pytest.mark.parametrize("counts,expected", [
    ({"spam": 0, "suspicious": 0, "clean": 0}, "empty"),
    ({"spam": 3, "suspicious": 0, "clean": 1}, "flooded"),
    ({"spam": 1, "suspicious": 1, "clean": 1}, "noisy"),
    ({"spam": 0, "suspicious": 1, "clean": 4}, "healthy"),
])
def test_inbox_status(counts, expected):
    assert inbox_status(counts) == expected
