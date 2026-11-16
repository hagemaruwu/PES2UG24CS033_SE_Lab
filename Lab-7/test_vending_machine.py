# Lab 7 tests. Bad input returns None; an empty coin list returns [].

import builtins

import pytest
from hypothesis import given, settings, strategies as st

from vending_machine import change_due, main, parse_coins, slot_position


DENOMINATIONS = (5, 10, 25, 50, 100)
FUZZ_SETTINGS = settings(
    max_examples=300, derandomize=True, deadline=None, report_multiple_bugs=False
)
NON_TEXT = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.binary(),
    st.lists(st.integers(), max_size=8),
    st.dictionaries(st.text(max_size=8), st.integers(), max_size=5),
    st.tuples(st.integers(), st.text(max_size=8)),
)
FUZZ_INPUTS = st.one_of(st.text(max_size=5000), NON_TEXT)


@FUZZ_SETTINGS
@given(FUZZ_INPUTS)
def test_parse_coins_no_crash(value):
    result = parse_coins(value)
    assert result is None or (
        isinstance(result, list)
        and all(type(coin) is int and coin in DENOMINATIONS for coin in result)
    )


@FUZZ_SETTINGS
@given(FUZZ_INPUTS)
def test_slot_position_no_crash(value):
    result = slot_position(value)
    assert result is None or (
        isinstance(result, tuple)
        and len(result) == 2
        and all(type(index) is int for index in result)
        and 0 <= result[0] < 26
        and result[1] >= 0
    )


@FUZZ_SETTINGS
@given(FUZZ_INPUTS)
def test_change_due_no_crash(value):
    result = change_due(value)
    if result is not None:
        assert isinstance(result, str)
        count, label = result.split(" ")
        assert count.isascii() and count.isdecimal()
        assert int(count) >= 0
        assert label == "five-coins"


@FUZZ_SETTINGS
@given(st.lists(st.sampled_from(DENOMINATIONS), max_size=1000))
def test_parse_coins_valid_round_trip(coins):
    csv = ",".join(str(coin) for coin in coins)
    assert parse_coins(csv) == coins
    assert parse_coins("  " + csv.replace(",", ", ") + "  ") == coins


@FUZZ_SETTINGS
@given(
    row=st.integers(min_value=0, max_value=25),
    column=st.integers(min_value=1, max_value=999999999999),
    lower_case=st.booleans(),
)
def test_slot_position_valid_round_trip(row, column, lower_case):
    letter = chr(ord("A") + row)
    if lower_case:
        letter = letter.lower()
    assert slot_position("  {}{}  ".format(letter, column)) == (row, column - 1)


@FUZZ_SETTINGS
@given(
    price=st.integers(min_value=0, max_value=1000000000),
    coin_count=st.integers(min_value=0, max_value=1000000),
)
def test_change_due_preserves_exact_value(price, coin_count):
    paid = price + coin_count * 5
    expected = "{} five-coins".format(coin_count)
    assert change_due("{} / {}".format(paid, price)) == expected


@FUZZ_SETTINGS
@given(st.integers(min_value=-1000000, max_value=1000000).filter(
    lambda coin: coin not in DENOMINATIONS
))
def test_parse_coins_rejects_unsupported_denominations(coin):
    assert parse_coins(str(coin)) is None


@FUZZ_SETTINGS
@given(
    price=st.integers(min_value=0, max_value=1000000000),
    count=st.integers(min_value=0, max_value=1000000),
    remainder=st.integers(min_value=1, max_value=4),
)
def test_change_due_does_not_silently_discard_remainder(price, count, remainder):
    assert change_due("{}/{}".format(price + count * 5 + remainder, price)) is None


@FUZZ_SETTINGS
@given(NON_TEXT)
def test_all_functions_reject_non_text(value):
    for function in (parse_coins, slot_position, change_due):
        assert function(value) is None


@pytest.mark.parametrize("value", ["", " ", "\t\n"])
def test_blank_coin_input_is_empty_list(value):
    assert parse_coins(value) == []


@pytest.mark.parametrize("value", [
    None, "5,,10", ",5", "5,", "one,two", "-5", "0", "1", "2", "20",
    "+5", "5.0", "5/10", "5,10,bad", "٥", "５", "5\x00", pytest.param("9" * 5000, id="5000-digit-number"),
])
def test_parse_coins_invalid_regressions(value):
    assert parse_coins(value) is None


@pytest.mark.parametrize("value", [
    None, "", " ", "A", "A0", "A-1", "A+1", "A1.0", "1A", "[1", "@1",
    "AA1", "A 1", "ß1", "é1", "Ａ1", "A١", "A１", "A1\x00",
    "A1000000000000", pytest.param("A" + "9" * 5000, id="oversized-slot"),
])
def test_slot_position_invalid_regressions(value):
    assert slot_position(value) is None


@pytest.mark.parametrize("value", [
    None, "", " ", "200", "200/", "/150", "200/150/5", "one/two",
    "-5/0", "10/-5", "+10/5", "10.5/5", "5/10", "9/5", "٢٠٠/١٥٠",
    "２００/１５０", "10/5\x00", "1000000000000/0", pytest.param("9" * 5000 + "/0", id="oversized-payment"),
])
def test_change_due_invalid_regressions(value):
    assert change_due(value) is None


@pytest.mark.parametrize("function, value, expected", [
    (parse_coins, " 5, 10,25,50,100 ", [5, 10, 25, 50, 100]),
    (slot_position, "B7", (1, 6)),
    (slot_position, "z1", (25, 0)),
    (slot_position, "A01", (0, 0)),
    (slot_position, "Z999999999999", (25, 999999999998)),
    (change_due, "200/150", "10 five-coins"),
    (change_due, "150/150", "0 five-coins"),
    (change_due, "0/0", "0 five-coins"),
    (change_due, "999999999999/999999999994", "1 five-coins"),
])
def test_valid_boundary_regressions(function, value, expected):
    assert function(value) == expected


@pytest.mark.parametrize("function", [parse_coins, slot_position, change_due])
def test_input_length_limit(function):
    assert function(" " * 4097) is None


def test_coin_count_limit():
    assert parse_coins(",".join(["5"] * 1000)) == [5] * 1000
    assert parse_coins(",".join(["5"] * 1001)) is None


@pytest.mark.parametrize("values, expected_fragments", [
    (["5,10,25", "B7", "200/150"],
     ["Coins: [5, 10, 25]", "Row and Column: (1, 6)", "Change Due: 10 five-coins"]),
    (["5,,10", "A0", "5/10"],
     ["Invalid coin input.", "Invalid slot code.", "Invalid payment or unavailable exact change."]),
])
def test_main_handles_valid_and_invalid_inputs(monkeypatch, capsys, values, expected_fragments):
    answers = iter(values)
    monkeypatch.setattr(builtins, "input", lambda prompt: next(answers))
    main()
    output = capsys.readouterr().out
    for fragment in expected_fragments:
        assert fragment in output


@pytest.mark.parametrize("exception", [EOFError, KeyboardInterrupt])
@pytest.mark.parametrize("position", [0, 1, 2])
def test_main_handles_cancelled_input(monkeypatch, capsys, exception, position):
    answers = iter(["5", "A1", "10/5"][:position])

    def interrupted_input(prompt):
        try:
            return next(answers)
        except StopIteration:
            raise exception()

    monkeypatch.setattr(builtins, "input", interrupted_input)
    try:
        main()
    except (EOFError, KeyboardInterrupt) as error:
        pytest.fail("main leaked {}".format(type(error).__name__))
    assert "Input cancelled." in capsys.readouterr().out
