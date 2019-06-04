from pynetest.lib.expectation import Expectation
from pynetest.lib.matchers.was_called_matcher import WasCalledMatcher
from pynetest.lib.matchers.was_called_with_matcher import WasCalledWithMatcher
from pynetest.lib.message_format_helper import format_arguments


class CalledExpectation(Expectation):
    def __init__(self):
        super().__init__("was_called", WasCalledMatcher())

    def message_format(self, subject, params):
        return "Expected that <{subject}> " + " ".join(self.name.split("_"))


class CalledWithExpectation(Expectation):
    def __init__(self, *args, **kwargs):
        super().__init__("was_called_with", WasCalledWithMatcher((args, kwargs)))

    def message_format(self, subject, params):
        param_list_formatting = " <" + format_arguments(params[0], params[1]) + ">"
        return "Expected that <{subject}> " + " ".join(self.name.split("_")) + param_list_formatting
