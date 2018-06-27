from .expectations import expect
import re
from .matchers import anything, match


def test__to_be__can_pass():
    expect(1).to_be(1)


def test__to_be__fails_with_message():
    exception = None
    try:
        expect(1).to_be(2)
    except AssertionError as e:
        exception = e
    finally:
        assert "Expected (1) to be (2)" == exception.args[0]


def test__to_be__with_a_matcher_can_pass():
    expect(anything()).to_be(1234)
    expect(1234).to_be(anything())


def test__not_to_be__can_pass():
    expect(3).not_to_be(4)
    expect(None).not_to_be("hello")


def test__not_to_be__when_equal__fails_with_message():
    expect(lambda: expect(1).not_to_be(1)).to_raise_error_message("Expected (1) not to be (1)")


def test__to_have_length__can_pass():
    expect([123, 123, 123]).to_have_length(3)


def test__to_have_length__fails_with_message():
    exception = None
    try:
        expect([123, 123, 123]).to_have_length(4)
    except AssertionError as e:
        exception = e
    finally:
        assert "Expected ([123, 123, 123]) to have length (4)" == exception.args[0]


def test__to_raise_error_message__can_pass():
    def error_method():
        raise Exception("some message")

    expect(error_method).to_raise_error_message("some message")


def test__to_raise_error_message__can_fail_because_the_message_is_wrong():
    def error_method():
        raise Exception("some other message")

    error = None
    try:
        expect(error_method).to_raise_error_message("some message")
    except AssertionError as e:
        error = e
    finally:
        assert re.search("but message was", error.args[0])


def test__to_raise_error_message__can_fail_because_no_error_is_raised():
    def error_method():
        pass

    error = None
    try:
        expect(error_method).to_raise_error_message("some message")
    except AssertionError as e:
        error = e
    finally:
        assert re.search("but no exception was raised", error.args[0])


def test__to_raise_error_message__can_pass_with_matcher():
    def error_method():
        raise Exception("some message")

    expect(error_method).to_raise_error_message(anything())


def test__to_be_a__can_pass():
    expect(1).to_be_a(int)
    expect('').to_be_a(str)

    class SomeClass:
        pass

    expect(SomeClass()).to_be_a(SomeClass)


def test__to_be_a__when_the_type_is_different__fails_with_message():
    class SomeClass:
        pass

    expect(lambda: expect('hello').to_be_a(SomeClass)).to_raise_error_message(
        match("Expected \(hello\) to be a .*SomeClass.*"))
