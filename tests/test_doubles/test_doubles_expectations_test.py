from pyne.expectations import expect
from pyne.test_doubles.spy import Spy
from pyne.test_doubles.stub import stub
from tests.test_helpers.expectation_helpers import expect_expectation_to_fail_with_message
from tests.test_helpers.some_class import SomeClass
from tests.test_helpers.temporary_class import TemporaryClass


def test__was_called_with__can_pass():
    spy = Spy()

    spy("some-positional-argument", ["some-array-content"])
    expect(spy).was_called_with("some-positional-argument", ["some-array-content"])


def test__for_an_instance_method__was_called_with__can_pass():
    some_instance = SomeClass()

    stub(some_instance, some_instance.some_method)

    some_instance.some_method("some-positional-argument", ["some-array-content"])
    expect(some_instance.some_method).was_called_with("some-positional-argument", ["some-array-content"])


def test__for_a_static_method__was_called_with__can_pass():
    with TemporaryClass() as SomeTemporaryClass:
        stub(SomeTemporaryClass, SomeTemporaryClass.some_static_method)

        SomeTemporaryClass.some_static_method("some-positional-argument", ["some-array-content"])
        expect(SomeTemporaryClass.some_static_method).was_called_with("some-positional-argument", ["some-array-content"])


def test__was_called_with__when_there_were_no_calls__fails_with_a_message():
    spy = Spy()

    expect_expectation_to_fail_with_message(
            lambda: expect(spy).was_called_with("some-positional-argument", ["some-array-content"]),
            "Expected that <spy> was called with <\('some-positional-argument', \['some-array-content'\]\)> but it was never called"
    )


def test__for_an_instance_method__was_called_with__when_there_were_no_calls__fails_with_a_message():
    some_instance = SomeClass()

    stub(some_instance, some_instance.some_method)

    expect_expectation_to_fail_with_message(
            lambda: expect(some_instance.some_method).was_called_with("some-positional-argument", ["some-array-content"]),
            "Expected that <SomeClass#some_method> was called with <\('some-positional-argument', \['some-array-content'\]\)> but it was never called"
    )


def test__for_a_static_method__was_called_with__when_there_were_no_calls__fails_with_a_message():
    with TemporaryClass() as SomeTemporaryClass:
        stub(SomeTemporaryClass, SomeTemporaryClass.some_static_method)

        expect_expectation_to_fail_with_message(
                lambda: expect(SomeTemporaryClass.some_static_method).was_called_with("some-positional-argument", ["some-array-content"]),
                "Expected that <SomeTemporaryClass::some_static_method> was called with <\('some-positional-argument', \['some-array-content'\]\)> but it was never called"
        )


def test__was_called_with__when_the_method_was_called_with_the_wrong_parameters__fails_with_a_message():
    spy = Spy()
    spy("some-positional-argument", "some-array-content")
    expect_expectation_to_fail_with_message(
            lambda: expect(spy).was_called_with("some-positional-argument", ["some-array-content"]),
            "Expected that <spy> was called with <\('some-positional-argument', \['some-array-content'\]\)> but it was called with <\('some-positional-argument', 'some-array-content'\)>"
    )


def test__for_an_instance_method__was_called_with__when_the_method_was_called_with_the_wrong_parameters__fails_with_a_message():
    some_instance = SomeClass()

    stub(some_instance, some_instance.some_method)

    some_instance.some_method("some-positional-argument", "some-array-content")
    expect_expectation_to_fail_with_message(
            lambda: expect(some_instance.some_method).was_called_with("some-positional-argument", ["some-array-content"]),
            "Expected that <SomeClass#some_method> was called with <\('some-positional-argument', \['some-array-content'\]\)> but it was called with <\('some-positional-argument', 'some-array-content'\)>"
    )


def test__for_a_static_method__was_called_with__when_the_method_was_called_with_the_wrong_parameters__fails_with_a_message():
    with TemporaryClass() as SomeTemporaryClass:
        stub(SomeTemporaryClass, SomeTemporaryClass.some_static_method)

        SomeTemporaryClass.some_static_method("some-positional-argument", "some-array-content")
        expect_expectation_to_fail_with_message(
                lambda: expect(SomeTemporaryClass.some_static_method).was_called_with("some-positional-argument", ["some-array-content"]),
                "Expected that <SomeTemporaryClass::some_static_method> was called with <\('some-positional-argument', \['some-array-content'\]\)> but it was called with <\('some-positional-argument', 'some-array-content'\)>"
        )


def test__was_called__can_pass():
    spy = Spy()

    spy()
    expect(spy).was_called()


def test__for_an_instance_method__was_called__can_pass():
    some_instance = SomeClass()

    stub(some_instance, some_instance.some_method)

    some_instance.some_method()
    expect(some_instance.some_method).was_called()


def test__for_a_static_method__was_called__can_pass():
    with TemporaryClass() as SomeTemporaryClass:
        stub(SomeTemporaryClass, SomeTemporaryClass.some_static_method)

        SomeTemporaryClass.some_static_method()
        expect(SomeTemporaryClass.some_static_method).was_called()


def test__was_called__when_there_were_no_calls__fails_with_a_message():
    spy = Spy()

    expect_expectation_to_fail_with_message(
            lambda: expect(spy).was_called(),
            "Expected that <spy> was called, but it was never called"
    )


def test__for_an_instance_method__was_called__when_there_were_no_calls__fails_with_a_message():
    some_instance = SomeClass()

    stub(some_instance, some_instance.some_method)

    expect_expectation_to_fail_with_message(
            lambda: expect(some_instance.some_method).was_called(),
            "Expected that <SomeClass#some_method> was called, but it was never called"
    )


def test__for_a_static_method__was_called__when_there_were_no_calls__fails_with_a_message():
    with TemporaryClass() as SomeTemporaryClass:
        stub(SomeTemporaryClass, SomeTemporaryClass.some_static_method)

        expect_expectation_to_fail_with_message(
                lambda: expect(SomeTemporaryClass.some_static_method).was_called(),
                "Expected that <SomeTemporaryClass::some_static_method> was called, but it was never called"
        )
