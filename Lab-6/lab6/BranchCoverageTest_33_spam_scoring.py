"""Lab 6: tests for branch coverage of spam_scoring.py."""

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


# Exercise empty loops, both sender-discount outcomes, and boundary values.
@pytest.mark.parametrize("text,known,links,expected", [
    ("", False, 0, 0),
    ("   ", True, 0, 0),
    ("free winner prize", True, 0, 3),
    ("free", True, 1, 0),
    ("free winner", True, 0, 1),
    ("hello", False, 3, 1),
    ("hello", False, 4, 4),
    ("HI ABC ABCD", False, 0, 1),
    ("FrEe, hello!", False, 0, 2),
    ("free free", False, 0, 4),
    ("free", False, 1, 3),
])
def test_scoring_branches_and_boundaries(text, known, links, expected):
    assert score_message(text, known, links) == expected


@pytest.mark.parametrize("score,expected", [
    (0, "clean"), (3, "clean"), (7, "suspicious"), (9, "spam"),
])
def test_classification_boundaries(score, expected):
    assert classify(score) == expected


def test_empty_inbox():
    assert filter_inbox([]) == {"spam": 0, "suspicious": 0, "clean": 0}


def test_known_sender_changes_classification():
    assert filter_inbox([("free winner prize urgent", True, 0)]) == {
        "spam": 0, "suspicious": 1, "clean": 0,
    }


@pytest.mark.parametrize("counts,expected", [
    ({"spam": 1, "suspicious": 0, "clean": 1}, "noisy"),  # exactly 50%
    ({"spam": 1, "suspicious": 0, "clean": 4}, "healthy"),  # exactly 20%
    ({"spam": 3, "suspicious": 0, "clean": 7}, "noisy"),
    ({"spam": 1, "suspicious": 0, "clean": 0}, "flooded"),
])
def test_ratio_boundaries(counts, expected):
    assert inbox_status(counts) == expected
