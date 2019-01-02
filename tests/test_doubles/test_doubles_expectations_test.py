# noinspection PyUnresolvedReferences
import pyne.test_doubles.test_double_expectations
from pyne.expectations import expect
from pyne.test_doubles.spy import stub
from tests.test_helpers import SomeClass, expect_expectation_to_fail_with_message


def test__was_called_with__can_pass():
    some_instance = SomeClass()

    stub(some_instance, some_instance.some_method)

    some_instance.some_method("some-positional-argument", ["some-array-content"])
    expect(some_instance.some_method).was_called_with("some-positional-argument", ["some-array-content"])


def test__was_called_with__when_there_were_no_calls__fails_with_a_message():
    some_instance = SomeClass()

    stub(some_instance, some_instance.some_method)

    expect_expectation_to_fail_with_message(
            lambda: expect(some_instance.some_method).was_called_with("some-positional-argument", ["some-array-content"]),
            "Expected that <SomeClass#some_method> was called with <\('some-positional-argument', \['some-array-content'\]\)> but it was never called"
    )


def test__was_called_with__when_the_method_was_called_with_the_wrong_parameters__fails_with_a_message():
    some_instance = SomeClass()

    stub(some_instance, some_instance.some_method)

    some_instance.some_method("some-positional-argument", "some-array-content")
    expect_expectation_to_fail_with_message(
            lambda: expect(some_instance.some_method).was_called_with("some-positional-argument", ["some-array-content"]),
            "Expected that <SomeClass#some_method> was called with <\('some-positional-argument', \['some-array-content'\]\)> but it was called with <\('some-positional-argument', 'some-array-content'\)>"
    )
