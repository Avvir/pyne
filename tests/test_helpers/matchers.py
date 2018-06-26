from termcolor import cprint


class Matchers:
    def __init__(self, subject):
        self.subject = subject
        self._to_be_matcher = Matcher("to_be", lambda actual, expected: (actual == expected))

    def to_be(self, expected):
        self._to_be_matcher.match(self.subject, expected)

    def not_to_be(self, expected):
        InverseMatcher(self._to_be_matcher).match(self.subject, expected)

    def to_have_length(self, length):
        self._to_have_length_matcher = Matcher("to_have_length", lambda subject, length: (len(subject) == length))
        self._to_have_length_matcher.match(self.subject, length)

    def to_raise_error_message(self, message):
        RaiseMatcher().match(self.subject, message)

class RaiseMatcher:
    def __init__(self):
        self.expected_message = None
        self.actual_exception = None

    def check_error(self, method, message):
        self.expected_message = message
        try:
            method()
        except Exception as e:
            self.actual_exception = e
            return e.args[0] == message

    def message_format(self):
        if self.actual_exception is None:
            return "Expected ({subject}) to raise an exception with message ({0}) but no exception was raised"
        else:
            return "Expected ({subject}) to raise an exception with message ({0}) but message was " + self.actual_exception.args[0]

    def match(self, subject, *params):
        return Matcher("to_raise_error_message", self.check_error, self.message_format).match(subject, *params)


class InverseMatcher:
    def __init__(self, matcher, message_format=None):
        self.matcher = matcher
        self.message_format = message_format

    def match(self, subject, *params):
        if self.matcher.comparator(subject, *params):
            message_format = self.default_message() if self.message_format is None else self.message_format()
            message = message_format.format(subject=subject, *params)
            cprint("\n" + message + "\n", 'yellow')
            raise Exception(message)

    def default_message(self):
        return "Expected ({subject}) not " + " ".join(self.name.split("_")) + " ({0})"


class Matcher:
    def __init__(self, name, comparator, message_format=None):
        self.name = name
        self.comparator = comparator
        self.message_format = message_format

    def match(self, subject, *params):
        if not self.comparator(subject, *params):
            message_format = self.default_message() if self.message_format is None else self.message_format()
            message = message_format.format(subject=subject, *params)
            cprint("\n" + message + "\n", 'yellow')
            raise Exception(message)

    def default_message(self):
        return "Expected ({subject}) " + " ".join(self.name.split("_")) + " ({0})"


def expect(subject):
    return Matchers(subject)
