import re


def expect_expectation_to_fail_with_message(expectation, message_regex):
    error = None
    try:
        expectation()
    except AssertionError as e:
        error = e
    finally:
        assert error is not None
        actual_message = error.args[0]
        if actual_message != message_regex:
            matches = re.search(message_regex, actual_message)
            if not matches:
                print("Expected regex: ", message_regex)
                print("Actual message: ", actual_message)
            assert matches
