from termcolor import cprint

from .matchers import InverseMatcher, Matcher, contains, equal_to, instance_of, is_matcher, is_none


class Expectations:
    def __init__(self, subject):
        self.subject = subject

    def to_be(self, expected):
        Expectation("to_be", equal_to(expected)).assert_expected(self.subject, expected)

    def not_to_be(self, expected):
        Expectation("to_be", equal_to(expected)).get_inverse().assert_expected(self.subject, expected)

    def to_have_length(self, length):
        length_matcher = Matcher("of_length", lambda subject, length: (equal_to(length).matches(len(subject))), length)
        to_have_length_expectation = Expectation("to_have_length", length_matcher)
        to_have_length_expectation.assert_expected(self.subject, length)

    def to_raise_error_with_message(self, message):
        RaiseMessageExpectation(message).assert_expected(self.subject, message)

    def to_raise_error_of_type(self, exception_class):
        RaiseTypeExpectation(exception_class).assert_expected(self.subject, exception_class)

    def to_be_a(self, class_):
        Expectation("to_be_a", instance_of(class_)).assert_expected(self.subject, class_)

    def to_contain(self, item_or_text):
        Expectation("to_contain", contains(item_or_text)).assert_expected(self.subject, item_or_text)

    def not_to_contain(self, item_or_text):
        expectation = Expectation("to_contain", contains(item_or_text)).get_inverse()
        expectation.assert_expected(self.subject, item_or_text)

    def to_be_none(self):
        expectation = Expectation("to_be_none", is_none())
        expectation.assert_expected(self.subject, ())

    def not_to_be_none(self):
        expectation = Expectation("to_be_none", is_none()).get_inverse()
        expectation.assert_expected(self.subject, ())


class Expectation:
    def __init__(self, name, matcher, message_format=None):
        self.name = name
        self.matcher = matcher
        self.message_format = message_format

    def get_inverse(self):
        return InverseExpectation(self)

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
    def __init__(self, error_matcher, message_format=None, exception_format=None):
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

    def message_format(self):
        if self.actual_exception is None:
            return "Expected <{subject}> to raise an exception " + self.error_description + " <{0}> but no exception was raised"
        else:
            return "Expected <{subject}> to raise an exception " + self.error_description + " <{0}> but the exception was <" + \
                   (self.escape_for_formatting("{0}".format(self.exception_format(self.actual_exception)))) + ">"


class RaiseMessageExpectation(RaiseExpectation):
    def __init__(self, *params):
        expected_message = params[0]
        message_matcher = Matcher("with_message",
                                  lambda exception, message:
                                  equal_to(message).matches(exception.args[0]),
                                  expected_message)
        super().__init__(message_matcher, exception_format=lambda e: e.args[0])


class RaiseTypeExpectation(RaiseExpectation):
    def __init__(self, *params):
        self.expected_type = params[0]
        self.inner_matcher = Matcher("of_type",
                                     lambda exception, clazz:
                                     instance_of(clazz).matches(exception),
                                     self.expected_type)
        super().__init__(self.inner_matcher)

    def message_format(self):
        if self.actual_exception is None:
            return "Expected <{subject}> to raise an exception of type <" + self.formatted_expected_type() + "> but no exception was raised"
        else:
            return "Expected <{subject}> to raise an exception of type <" + self.formatted_expected_type() + "> but the exception was <" + \
                   (self.escape_for_formatting("{0}".format(self.exception_format(self.actual_exception)))) + ">"

    def formatted_expected_type(self):
        return self.expected_type.__name__


class InverseExpectation(Expectation):
    def __init__(self, expectation):
        name = "not_" + expectation.name
        matcher = InverseMatcher("not_" + expectation.matcher.name, expectation.matcher)
        super().__init__(name, matcher)


def expect(subject):
    return Expectations(subject)
