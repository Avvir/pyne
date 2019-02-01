class Matcher:
    def __init__(self, name, comparator, *params):
        self.name = name
        self.comparator = comparator
        self.params = params
        self._reason = None

    def matches(self, subject):
        return self.comparator(subject, *self.params)

    def reason(self):
        return None

    def format(self):
        return "{matcher_name}{params}".format(matcher_name=self.name, params=self.params)


class InverseMatcher(Matcher):
    def __init__(self, name, comparator, *params):
        super().__init__(name, lambda subject: not comparator.matches(subject), *params)


def is_matcher(possible_matcher):
    return isinstance(possible_matcher, Matcher)


def equal_to_comparator(subject, *params):
    if is_matcher(subject):
        return subject.matches(params[0])
    elif is_matcher(params[0]):
        return params[0].matches(subject)
    else:
        return subject == params[0]