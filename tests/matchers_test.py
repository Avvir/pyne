from pynetest.expectations import expect
from pynetest.matchers import anything, at_least, contains, contains_text, has_length, instance_of, match, between, about, \
    at_most


def test__anything__satisfies_to_be():
    expect(anything()).to_be(1234)
    expect(1234).to_be(anything())


def test__match__can_match_regex():
    expect("hello (world)").to_be(match("h.*\\(world\\)"))


def test__match__when_string_is_different__does_not_match():
    expect("hello world").not_to_be(match("happy.*world"))


def test__contains_text__can_match_text():
    expect("hello world").to_be(contains_text("world"))


def test__between__can_pass():
    expect(1).to_be(between(0, 4))


def test__contains_text__when_string_is_different__does_not_match():
    expect("hello world").not_to_be(contains_text(".*"))


def test__contains_text__when_subject_is_not_iterable__does_not_match():
    expect(None).not_to_be(contains_text("world"))


def test__contains__can_match_array():
    expect(["some-other-item", "some-item"]).to_be(contains("some-item"))


def test__contains__when_subject_is_not_iterable__does_not_match():
    expect(None).not_to_be(contains("world"))


def test__instance_of__can_match_type():
    expect("hello").to_be(instance_of(str))


def test__instance_of__when_subject_is_different_type__does_not_match():
    expect("hello").not_to_be(instance_of(int))


def test__at_least__matches_a_larger_number():
    expect(2).to_be(at_least(1))


def test__at_least__when_numbers_are_equal__matches():
    expect(2).to_be(at_least(2))


def test__at_least__when_number_is_smaller__does_not_match():
    expect(1).not_to_be(at_least(2))


def test__at_most__matches_a_smaller_number():
    expect(1).to_be(at_most(2))


def test__at_most__when_numbers_are_equal__matches():
    expect(2).to_be(at_most(2))


def test__at_most__when_number_is_larger__does_not_match():
    expect(2).not_to_be(at_most(1))


def test__has_length__matches_anything_with_length():
    expect(str("string")).to_be(has_length(6))
    expect(list([1, 2, 3])).to_be(has_length(3))
    expect((1, 2)).to_be(has_length(2))
    expect(range(10)).to_be(has_length(10))
    expect(bytes(8)).to_be(has_length(8))
    expect(bytearray(7)).to_be(has_length(7))
    expect(dict(key="value")).to_be(has_length(1))
    expect(set()).to_be(has_length(0))
    expect(frozenset(range(9))).to_be(has_length(9))


def test__has_length__when_length_is_different__does_not_match():
    expect("string").not_to_be(has_length(2))


def test__about__matches_numbers_within_a_given_tolerance():
    expect(3.000001).to_be(about(3, 0.001))


def test__about__when_no_tolerance_is_given__matches_numbers_within_one_thousandth_of_the_number():
    expect(3.0001).to_be(about(3))


def test__about__when_number_is_outside_tolerance__does_not_match():
    expect(3.5).not_to_be(about(3))
