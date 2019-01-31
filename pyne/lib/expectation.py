from termcolor import cprint

from pyne.lib.matcher import InverseMatcher
from pyne.matchers import is_matcher


class Expectation:
    def __init__(self, name, matcher, message_format=None):
        self.name = name
        self.matcher = matcher
        self._message_format = message_format

    def get_inverse(self):
        return InverseExpectation(self)

    def message_format(self, subject, params):
        if self._message_format is None:
            return self.default_message()
        else:
            return self._message_format

    def assert_expected(self, subject, *params):
        if not self.matcher.matches(subject):
            message_format = self.message_format(subject, params)
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


class InverseExpectation(Expectation):
    def __init__(self, expectation):
        name = "not_" + expectation.name
        matcher = InverseMatcher("not_" + expectation.matcher.name, expectation.matcher)

        inverted_message = None
        if expectation._message_format:
            inverted_message = self.invert_message(expectation._message_format)

        super().__init__(name, matcher, message_format=inverted_message)

    def invert_message(self, message):
        return message.replace(" to ", " not to ")
