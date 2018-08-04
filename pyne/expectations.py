from termcolor import cprint
from .matchers import Matcher, InverseMatcher, equal_to, is_matcher, contains, instance_of


class Expectations:
    def __init__(self, subject):
        self.subject = subject

    def to_be(self, expected):
        Expectation("to_be", equal_to(expected)).assert_expected(self.subject, expected)

    def not_to_be(self, expected):
        InverseExpectation(Expectation("to_be", equal_to(expected))).assert_expected(self.subject, expected)

    def to_have_length(self, length):
        length_matcher = Matcher("of_length", lambda subject, length: (equal_to(length).matches(len(subject))), length)
        to_have_length_expectation = Expectation("to_have_length", length_matcher)
        to_have_length_expectation.assert_expected(self.subject, length)

    def to_raise_error_message(self, message):
        RaiseExpectation(message).assert_expected(self.subject, message)

    def to_be_a(self, clazz):
        Expectation("to_be_a", instance_of(clazz)).assert_expected(self.subject, clazz)

    def to_contain(self, item_or_text):
        Expectation("to_contain", contains(item_or_text)).assert_expected(self.subject, item_or_text)


class Expectation:
    def __init__(self, name, matcher, message_format=None):
        self.name = name
        self.matcher = matcher
        self.message_format = message_format

    def assert_expected(self, subject, *params):
        if not self.matcher.matches(subject):
            message_format = self.default_message() if self.message_format is None else self.message_format()
            formatted_params, formatted_subject = self.unmatcherify(params, subject)
            message = message_format.format(*formatted_params, subject=formatted_subject)
            cprint("\n" + message + "\n", 'yellow')
            raise AssertionError(message)

    def default_message(self):
        return "Expected <{subject}> " + " ".join(self.name.split("_")) + " <{0}>"

    def unmatcherify(self, params, subject):
        formatted_subject = subject
        formatted_params = []
        if is_matcher(subject):
            formatted_subject = subject.format()
        for param in params:
            if is_matcher(param):
                formatted_params.append(param.format())
            else:
                formatted_params.append(param)
        return formatted_params, formatted_subject

    def escape_for_formatting(self, string):
        return string.replace("{", "{{").replace("}", "}}")


class RaiseExpectation(Expectation):
    def __init__(self, *params):
        self.expected_message = params[0]
        self.actual_exception = None
        super().__init__("to_raise_error_message", Matcher("raises_error_message", self.check_error, params[0]),
                         self.message_format)

    def check_error(self, method, message):
        self.expected_message = message
        try:
            method()
        except Exception as e:
            self.actual_exception = e
            return equal_to(e.args[0]).matches(message)

    def message_format(self):
        if self.actual_exception is None:
            return "Expected <{subject}> to raise an exception with message <{0}> but no exception was raised"
        else:
            return "Expected <{subject}> to raise an exception with message <{0}> but message was <" + \
                   (self.escape_for_formatting("{0}".format(self.actual_exception.args[0]))) + ">"


class InverseExpectation(Expectation):
    def __init__(self, expectation):
        name = "not_" + expectation.name
        matcher = InverseMatcher("not_" + expectation.matcher.name, expectation.matcher)
        super().__init__(name, matcher)


def expect(subject):
    return Expectations(subject)
