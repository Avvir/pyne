from pynetest.expectations import expect
from pynetest.matchers import anything
from pynetest.test_doubles.test_double_matchers import was_called_with
from pynetest.test_doubles.stub import spy_on
from tests.test_helpers.expectation_helpers import expect_expectation_to_fail_with_message
from tests.test_helpers.some_class import SomeClass


def test__was_called_with_matcher__can_pass():
    some_instance = SomeClass()

    spy_on(some_instance.some_method)

    some_instance.some_method("some-positional-argument", ["some-array-content"])
    expect(some_instance.some_method).to_be(was_called_with("some-positional-argument", ["some-array-content"]))


def test__was_called_with_matcher__when_there_were_no_calls__fails_with_a_message():
    some_instance = SomeClass()

    spy_on(some_instance.some_method)

    expect_expectation_to_fail_with_message(
        lambda: expect(some_instance.some_method).to_be(
            was_called_with("some-positional-argument", ["some-array-content"])),
        "Expected <.*> to be <was_called_with\\(.*>"
    )


def test__was_called_with_matcher__when_the_method_was_called_with_the_different_arguments__fails_with_a_message():
    some_instance = SomeClass()

    spy_on(some_instance.some_method)

    some_instance.some_method("some-positional-argument", "some-array-content")
    expect_expectation_to_fail_with_message(
        lambda: expect(some_instance.some_method).to_be(
            was_called_with("some-positional-argument", ["some-array-content"])),
        "Expected <.*> to be <was_called_with\\(.*>"
    )


def test__was_called_with_matcher__when_the_method_was_called_with_different_keyword_args__fails_with_a_message():
    some_instance = SomeClass()

    spy_on(some_instance.some_method)

    some_instance.some_method(some_keyword_arg="some-value")

    expect_expectation_to_fail_with_message(
        lambda: expect(some_instance.some_method).to_be(was_called_with(some_keyword_arg="some-other-value")),
        "Expected <.*> to be <was_called_with\\(.*>"
    )


def test__was_called_with_matcher__when_a_positional_arg_was_passed_in_keyword_style__can_pass_with_keyword_style_expectation():
    some_instance = SomeClass()

    spy_on(some_instance.some_positional_args_method)

    some_instance.some_positional_args_method(some_first_arg="some-value")
    expect(some_instance.some_positional_args_method).to_be(was_called_with(some_first_arg="some-value"))


def test__was_called_with_matcher__when_a_positional_arg_was_passed_in_keyword_style__can_pass_with_positional_style_expectation():
    some_instance = SomeClass()

    spy_on(some_instance.some_other_method)

    some_instance.some_other_method(some_first_arg="some-value")
    expect(some_instance.some_other_method).to_be(was_called_with("some-value"))


def test__was_called_with_matcher__supports_matchers_for_positional_arguments():
    some_instance = SomeClass()

    spy_on(some_instance.some_method)

    some_instance.some_method("some-positional-argument", ["some-array-content"])
    expect(some_instance.some_method).to_be(was_called_with(anything(), ["some-array-content"]))
