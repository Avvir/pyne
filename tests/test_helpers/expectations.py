from termcolor import cprint
from .matchers import Matcher, equal_to

class Expectations:
    def __init__(self, subject):
        self.subject = subject
        self._to_be_expectation = Expectation("to_be", equal_to)

    def to_be(self, expected):
        self._to_be_expectation.assert_expected(self.subject, expected)

    def not_to_be(self, expected):
        InverseExpectation(self._to_be_expectation).assert_expected(self.subject, expected)

    def to_have_length(self, length):
        length_matcher = Matcher(lambda subject, length: (len(subject) == length))
        to_have_length_expectation = Expectation("to_have_length", length_matcher)
        to_have_length_expectation.assert_expected(self.subject, length)

    def to_raise_error_message(self, message):
        RaiseExpectation().assert_expected(self.subject, message)

    def to_be_a(self, clazz):
        instance_matcher = Matcher(lambda subject, clazz: isinstance(subject, clazz))
        Expectation("to_be_a", instance_matcher).assert_expected(self.subject, clazz)

class RaiseExpectation:
    def __init__(self):
        self.expected_message = None
        self.actual_exception = None

    def check_error(self, method, message):
        self.expected_message = message
        try:
            method()
        except Exception as e:
            self.actual_exception = e
            return equal_to.matches(e.args[0], message)

    def message_format(self):
        if self.actual_exception is None:
            return "Expected ({subject}) to raise an exception with message ({0}) but no exception was raised"
        else:
            return "Expected ({subject}) to raise an exception with message ({0}) but message was " + \
                   self.actual_exception.args[0]

    def assert_expected(self, subject, *params):
        return Expectation("to_raise_error_message", Matcher(self.check_error), self.message_format).assert_expected(subject,
                                                                                                            *params)


class InverseExpectation:
    def __init__(self, matcher, message_format=None):
        self.matcher = matcher
        self.message_format = message_format

    def assert_expected(self, subject, *params):
        if self.matcher.matches(subject, *params):
            message_format = self.default_message() if self.message_format is None else self.message_format()
            message = message_format.format(subject=subject, *params)
            cprint("\n" + message + "\n", 'yellow')
            raise AssertionError(message)

    def default_message(self):
        return "Expected ({subject}) not " + " ".join(self.name.split("_")) + " ({0})"


class Expectation:
    def __init__(self, name, matcher, message_format=None):
        self.name = name
        self.matcher = matcher
        self.message_format = message_format

    def assert_expected(self, subject, *params):
        if not self.matcher.matches(subject, *params):
            message_format = self.default_message() if self.message_format is None else self.message_format()
            message = message_format.format(subject=subject, *params)
            cprint("\n" + message + "\n", 'yellow')
            raise AssertionError(message)

    def default_message(self):
        return "Expected ({subject}) " + " ".join(self.name.split("_")) + " ({0})"

def expect(subject):
    return Expectations(subject)
