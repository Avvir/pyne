from termcolor import cprint

from pynetest.lib.matcher import InverseMatcher
from pynetest.lib.message_format_helper import format_object


class Expectation:
    def __init__(self, name, matcher, message_format=None):
        self.name = name
        self.matcher = matcher
        self._message_format = message_format

    def get_inverse(self):
        return InverseExpectation(self)

    def message_format(self, subject, params):
        if self._message_format is None:
            return self.default_message(len(params))
        else:
            return self._message_format

    def assert_expected(self, subject, *params):
        reason = None
        try:
            matches = self.matcher.matches(subject)
        except Exception as e:
            matches = False
            reason = "matcher raised <" + str(type(e).__name__) + ": " + str(e) + ">"

        if not matches:
            message_format = self.message_format(subject, params)
            formatted_params, formatted_subject = self.unmatcherify(params, subject)
            escaped_message = message_format.format(*formatted_params, subject=formatted_subject)
            unescaped_message = self.unescape_for_formatting(escaped_message)
            reason = reason or self.matcher.reason()
            if reason is not None:
                unescaped_message += " but " + reason
            cprint("\n" + unescaped_message + "\n", 'yellow')
            raise AssertionError(unescaped_message)

    def default_message(self, param_count=1):
        if param_count == 0:
            return "Expected <{subject}> " + " ".join(self.name.split("_"))
        elif param_count == 1:
            return "Expected <{subject}> " + " ".join(self.name.split("_")) + " <{0}>"
        else:
            param_list_formatting = " <" + ", ".join(["<{" + str(i) + "}>" for i in range(param_count)]) + ">"
            return "Expected <{subject}> " + " ".join(self.name.split("_")) + param_list_formatting

    def unmatcherify(self, params, subject):
        formatted_params = []
        formatted_subject = format_object(subject)
        for param in params:
            formatted_params.append(format_object(param))
        return formatted_params, formatted_subject

    def escape_for_formatting(self, string):
        return string.replace("{", "{{").replace("}", "}}")

    def unescape_for_formatting(self, string):
        return string.replace("{{", "{").replace("}}", "}")


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
