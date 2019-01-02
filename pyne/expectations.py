from pyne.expectation import Expectation
from pyne.test_doubles.test_double_expectations import CalledWithExpectation
from pyne.test_doubles.test_double_matchers import was_called_with
from .matchers import Matcher, contains, equal_to, instance_of, is_none, has_length, between


class Expectations:
    def __init__(self, subject):
        self.subject = subject

    def to_be(self, expected):
        Expectation("to_be", equal_to(expected)).assert_expected(self.subject, expected)

    def not_to_be(self, expected):
        Expectation("to_be", equal_to(expected)).get_inverse().assert_expected(self.subject, expected)

    def to_have_length(self, length):
        Expectation("to_have_length", has_length(length)).assert_expected(self.subject, length)

    def not_to_have_length(self, length):
        Expectation("to_have_length", has_length(length)).get_inverse().assert_expected(self.subject, length)

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
        expectation = Expectation("to_be_none", is_none(), message_format="Expected <{subject}> to be None")
        expectation.assert_expected(self.subject)

    def not_to_be_none(self):
        expectation = Expectation("to_be_none", is_none(),
                                  message_format="Expected <{subject}> to be None").get_inverse()
        expectation.assert_expected(self.subject)

    def to_be_between(self, lower, upper):
        expectation = ToBeBetweenExpectation(lower, upper)
        expectation.assert_expected(self.subject, lower, upper)

    def was_called_with(self, *args, **kwargs):
        CalledWithExpectation(was_called_with(*args, **kwargs)).assert_expected(self.subject, args, kwargs)


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

    def message_format(self, subject, params):
        if self.actual_exception is None:
            return "Expected <{subject}> to raise an exception of type <" + self.formatted_expected_type() + "> but no exception was raised"
        else:
            return "Expected <{subject}> to raise an exception of type <" + self.formatted_expected_type() + "> but the exception was <" + \
                   (self.escape_for_formatting("{0}".format(self.exception_format(self.actual_exception)))) + ">"

    def formatted_expected_type(self):
        return self.expected_type.__name__


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


def expect(subject):
    return Expectations(subject)
