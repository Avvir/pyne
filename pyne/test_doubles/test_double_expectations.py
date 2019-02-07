from termcolor import cprint

from pyne.lib.expectation import Expectation


def format_tuple_as_args(args_tuple):
    if len(args_tuple) is 1:
        formatted_args = str(args_tuple)[1:-2]
    else:
        formatted_args = str(args_tuple)[1:-1]
    return formatted_args


def format_params(args_tuple, kwargs_dict):
    formatted_args = format_tuple_as_args(args_tuple)
    if len(kwargs_dict) > 0:
        formatted_kwargs = str(kwargs_dict)[1:-1]
        params = formatted_args + ", " + formatted_kwargs
    else:
        params = formatted_args
    return params


def format_subject(method, subject):
    stubbed_object = subject.stubbed_object
    if stubbed_object is None:
        formatted_subject = "spy"
    elif isinstance(stubbed_object, type):
        formatted_subject = stubbed_object.__name__ + "::" + method.__name__
    else:
        formatted_subject = stubbed_object.__class__.__name__ + "#" + method.__name__
    return formatted_subject


class CalledExpectation(Expectation):
    def __init__(self):
        super().__init__("to_be_called", None)

    def assert_expected(self, subject, *params):
        if subject.last_call is None:
            method = subject.method
            formatted_subject = format_subject(method, subject)
            message = "Expected that <{subject}> was called, but it was never called".format(subject=formatted_subject)
            cprint("\n" + message + "\n", "yellow")
            raise AssertionError(message)


class CalledWithExpectation(Expectation):
    def __init__(self, matcher):
        super().__init__("to_be_called_with", matcher)

    def assert_expected(self, subject, *params):
        if not self.matcher.matches(subject):
            expected_args = params[0]
            expected_kwargs = params[1]
            method = subject.method

            formatted_subject = format_subject(method, subject)
            expected_params = format_params(expected_args, expected_kwargs)

            if subject.last_call is not None:
                actual_args = subject.last_call[0]
                actual_kwargs = subject.last_call[1]

                actual_params = format_params(actual_args, actual_kwargs)

                message = "Expected that <{subject}> was called with <({expected_params})> but it was called with <({actual_params})>".format(
                        expected_params=expected_params,
                        actual_params=actual_params,
                        subject=formatted_subject)
            else:
                message = "Expected that <{subject}> was called with <({expected_params})> but it was never called".format(
                        expected_params=expected_params,
                        subject=formatted_subject)

            cprint("\n" + message + "\n", 'yellow')
            raise AssertionError(message)
