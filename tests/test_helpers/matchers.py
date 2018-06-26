from termcolor import cprint


class Matchers:
    def __init__(self, actual):
        self.actual = actual
        self.to_be_matcher = Matcher("to_be", lambda actual, expected: (actual == expected))

    def to_be(self, expected):
        self.to_be_matcher.match(self.actual, expected)

    def not_to_be(self, expected):
        InverseMatcher(self.to_be_matcher).match(self.actual, expected)


class InverseMatcher:
    def __init__(self, matcher, message_format=None):
        self.matcher = matcher
        self.message_format = message_format

    def match(self, actual, *params):
        if self.matcher.comparator(actual, *params):
            message_format = self.default_message() if self.message_format is None else self.message_format
            message = message_format.format(actual=actual, *params)
            cprint("\n" + message + "\n", 'yellow')
            raise Exception(message)

    def default_message(self):
        return "Expected ({actual}) not " + " ".join(self.name.split("_")) + " ({0})"


class Matcher:
    def __init__(self, name, comparator, message_format=None):
        self.name = name
        self.comparator = comparator
        self.message_format = message_format

    def match(self, actual, *params):
        if not self.comparator(actual, *params):
            message_format = self.default_message() if self.message_format is None else self.message_format
            message = message_format.format(actual=actual, *params)
            cprint("\n" + message + "\n", 'yellow')
            raise Exception(message)

    def default_message(self):
        return "Expected ({actual}) " + " ".join(self.name.split("_")) + " ({0})"


def expect(actual):
    return Matchers(actual)
