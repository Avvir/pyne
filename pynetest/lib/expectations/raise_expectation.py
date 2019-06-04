from pynetest.lib.expectation import Expectation
from pynetest.lib.matcher import Matcher


class RaiseExpectation(Expectation):
    def __init__(self, error_matcher, exception_format=None):
        if exception_format is None:
            exception_format = lambda e: repr(e)
        matcher_name = error_matcher.name
        name = "to_raise_error_" + matcher_name
        self.actual_exception = None
        self.error_description = matcher_name.replace("_", " ")
        super().__init__(name, Matcher(matcher_name, self.check_error),
                         self.message_format)
        self.error_matcher = error_matcher
        self.exception_format = exception_format

    def check_error(self, method):
        try:
            method()
        except Exception as e:
            self.actual_exception = e
            return self.error_matcher.matches(e)

    def message_format(self, subject, params):
        if self.actual_exception is None:
            return "Expected <{subject}> to raise an exception " + self.error_description + " <{0}> but no exception was raised"
        else:
            return "Expected <{subject}> to raise an exception " + self.error_description + " <{0}> but the exception was <" + \
                   (self.escape_for_formatting("{0}".format(self.exception_format(self.actual_exception)))) + ">"