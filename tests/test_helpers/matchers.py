import re


class Matcher:
    def __init__(self, comparator, *params):
        self.comparator = comparator
        self.params = params

    def matches(self, subject):
        return self.comparator(subject, *self.params)


class InverseMatcher(Matcher):
    def __init__(self, comparator, *params):
        super().__init__(lambda subject: not comparator.matches(subject), *params)


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


def match(regular_expression):
    return Matcher(lambda subject, *params: re.search(params[0], subject), regular_expression)
