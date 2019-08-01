from pynetest.lib.expectation import Expectation
from pynetest.lib.expectations.raise_message_expectation import RaiseMessageExpectation
from pynetest.lib.expectations.raise_type_expectation import RaiseTypeExpectation
from pynetest.lib.expectations.to_be_between_expectation import ToBeBetweenExpectation
from pynetest.matchers import contains, equal_to, has_length, instance_of, is_none, about, matches_list
from pynetest.test_doubles.test_double_expectations import CalledExpectation, CalledWithExpectation, \
    NotCalledExpectation


class PossibleExpectations:
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
        expectation = Expectation("to_be_none", is_none(), message_format="Expected <{subject}> to be None").get_inverse()
        expectation.assert_expected(self.subject)

    def to_be_between(self, lower, upper):
        expectation = ToBeBetweenExpectation(lower, upper)
        expectation.assert_expected(self.subject, lower, upper)

    def to_be_about(self, number, tolerance=0.001):
        expectation = Expectation("to_be_about", about(number, tolerance), message_format="Expected <{subject}> to be about <{0}>")
        expectation.assert_expected(self.subject, number, tolerance)

    def was_called(self):
        CalledExpectation().assert_expected(self.subject)

    def was_not_called(self):
        NotCalledExpectation().assert_expected(self.subject)

    def was_called_with(self, *args, **kwargs):
        CalledWithExpectation(*args, **kwargs).assert_expected(self.subject, args, kwargs)

    def to_match_list(self, expected_list):
        expectation = Expectation("to_match_list", matches_list(expected_list))
        expectation.assert_expected(self.subject, expected_list)


def expect(subject):
    return PossibleExpectations(subject)
