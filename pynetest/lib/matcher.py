from pynetest.lib.message_format_helper import format_arguments


class Matcher:
    def __init__(self, name, comparator, *params):
        self.name = name
        self.comparator = comparator
        self.params = params
        self._reason = None

    def matches(self, subject):
        try:
            matches = self.comparator(subject, *self.params)
        except Exception as e:
            matches = False
            self._reason = "comparator raised <" + str(type(e).__name__) + ": " + str(e) + ">"
        return matches

    def reason(self):
        return self._reason

    def _pyne_format(self):
        return self.format()

    def format(self):
        return "{matcher_name}{params}".format(matcher_name=self.name, params=format_arguments(self.params))


class InverseMatcher(Matcher):
    def __init__(self, name, comparator, *params):
        super().__init__(name, lambda subject: not comparator.matches(subject), *params)


class EqualToMatcher(Matcher):
    def __init__(self, *params):
        super().__init__("equal_to", self.comparator, *params)

    def comparator(self, subject, *params):
        if len(params) == 0:
            self._reason = "there was nothing to compare to"
            return False
        if is_matcher(subject):
            matches = subject.matches(params[0])
            self._reason = subject.reason()
            return matches
        elif is_matcher(params[0]):
            matches = params[0].matches(subject)
            self._reason = params[0].reason()
            return matches
        else:
            return subject == params[0]


def is_matcher(possible_matcher):
    return isinstance(possible_matcher, Matcher)


def equal_to_comparator(subject, *params):
    if is_matcher(subject):
        return subject.matches(params[0])
    elif is_matcher(params[0]):
        return params[0].matches(subject)
    else:
        return subject == params[0]
