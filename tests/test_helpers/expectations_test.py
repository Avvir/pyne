from .expectations import expect
import re

def test__to_be__can_pass():
    expect(1).to_be(1)


def test__to_be__fails_with_message():
    exception = None
    try:
        expect(1).to_be(2)
    except Exception as e:
        exception = e
    finally:
        assert "Expected (1) to be (2)" == exception.args[0]


def test__to_have_length__can_pass():
    expect([123, 123, 123]).to_have_length(3)


def test__to_have_length__fails_with_message():
    exception = None
    try:
        expect([123, 123, 123]).to_have_length(4)
    except Exception as e:
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
    except Exception as e:
        error = e
    finally:
        assert re.search("but message was", error.args[0])


def test__to_raise_error_message__can_fail_because_no_error_is_raised():
    def error_method():
        pass

    error = None
    try:
        expect(error_method).to_raise_error_message("some message")
    except Exception as e:
        error = e
    finally:
        assert re.search("but no exception was raised", error.args[0])
