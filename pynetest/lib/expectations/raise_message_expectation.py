from pynetest.lib.matcher import Matcher
from pynetest.lib.expectations.raise_expectation import RaiseExpectation
from pynetest.matchers import equal_to


class RaiseMessageExpectation(RaiseExpectation):
    def __init__(self, *params):
        expected_message = params[0]
        message_matcher = Matcher("with_message",
                                  lambda exception, message:
                                  equal_to(message).matches(exception.args[0]),
                                  expected_message)
        super().__init__(message_matcher, exception_format=lambda e: e.args[0])