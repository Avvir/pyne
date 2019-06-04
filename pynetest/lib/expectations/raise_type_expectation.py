from pynetest.lib.matcher import Matcher
from pynetest.lib.expectations.raise_expectation import RaiseExpectation
from pynetest.matchers import instance_of


class RaiseTypeExpectation(RaiseExpectation):
    def __init__(self, *params):
        self.expected_type = params[0]
        self.inner_matcher = Matcher("of_type",
                                     lambda exception, clazz:
                                     instance_of(clazz).matches(exception),
                                     self.expected_type)
        super().__init__(self.inner_matcher)

    def message_format(self, subject, params):
        if self.actual_exception is None:
            return "Expected <{subject}> to raise an exception of type <" + self.formatted_expected_type() + "> but no exception was raised"
        else:
            return "Expected <{subject}> to raise an exception of type <" + self.formatted_expected_type() + "> but the exception was <" + \
                   (self.escape_for_formatting("{0}".format(self.exception_format(self.actual_exception)))) + ">"

    def formatted_expected_type(self):
        return self.expected_type.__name__