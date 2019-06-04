from pynetest.lib.expectation import Expectation
from pynetest.matchers import between


class ToBeBetweenExpectation(Expectation):
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper
        super().__init__("to_be_between", between(lower, upper), self.message_format)

    def message_format(self, subject, params):
        lower, upper = params
        if subject < lower:
            return "Expected <{subject}> to be between <{0}> and <{1}> " \
                   "but it was less than or equal to <{0}>"
        else:
            return "Expected <{subject}> to be between <{0}> and <{1}> " \
                   "but it was greater than or equal to <{1}>"
