from termcolor import cprint

from pyne.lib.expectation import Expectation
from pyne.lib.matchers.was_called_with_matcher import WasCalledWithMatcher
from pyne.lib.message_format_helper import format_arguments


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
        super().__init__("was_called", None)

    def assert_expected(self, subject, *params):
        if subject.last_call is None:
            method = subject.original_method
            formatted_subject = format_subject(method, subject)
            message = "Expected that <{subject}> was called, but it was never called".format(subject=formatted_subject)
            cprint("\n" + message + "\n", "yellow")
            raise AssertionError(message)


class CalledWithExpectation(Expectation):
    def __init__(self, *args, **kwargs):
        super().__init__("was_called_with", WasCalledWithMatcher((args, kwargs)))

    def message_format(self, subject, params):

        param_list_formatting = " <" + format_arguments(params[0], params[1]) + ">"
        return "Expected that <{subject}> " + " ".join(self.name.split("_")) + param_list_formatting

