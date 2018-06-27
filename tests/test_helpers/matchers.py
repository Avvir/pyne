class Matcher:
    def __init__(self, comparator):
        self.comparator = comparator

    def matches(self, subject, *params):
        return self.comparator(subject, *params)


def is_matcher(possible_matcher):
    return isinstance(possible_matcher, Matcher)


def equal_to_comparator(subject, *params):
    if is_matcher(subject):
        return subject.matches(params[0])
    elif is_matcher(params[0]):
        return params[0].matches(subject)
    else:
        return subject == params[0]


equal_to = Matcher(equal_to_comparator)
anything = Matcher(lambda subject, *params: True)
