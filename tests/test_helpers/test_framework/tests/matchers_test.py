from tests.test_helpers.test_framework.expectations import expect
from tests.test_helpers.test_framework.matchers import anything, match, contains_text


def test__anything__satisfies_to_be():
    expect(anything()).to_be(1234)
    expect(1234).to_be(anything())


def test__match__can_match_regex():
    expect("hello (world)").to_be(match("h.*\(world\)"))


def test__match__when_string_is_different__does_not_match():
    expect("hello world").not_to_be(match("happy.*world"))


def test__contains_text__can_match_text():
    expect("hello world").to_be(contains_text("world"))


def test__contains_text__when_string_is_different__does_not_match():
    expect("hello world").not_to_be(contains_text(".*"))
