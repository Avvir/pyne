class Matcher:
    def __init__(self, comparator, *params):
        self.comparator = comparator
        self.params = params

    def matches(self, subject):
        return self.comparator(subject, *self.params)


def is_matcher(possible_matcher):
    return isinstance(possible_matcher, Matcher)


def equal_to_comparator(subject, *params):
    if is_matcher(subject):
        return subject.matches(params[0])
    elif is_matcher(params[0]):
        return params[0].matches(subject)
    else:
        return subject == params[0]


def equal_to(value):
    return Matcher(equal_to_comparator, value)


def anything():
    return Matcher(lambda subject, *params: True)
