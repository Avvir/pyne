import re

from pynetest.lib.matcher import Matcher, is_matcher, equal_to_comparator, EqualToMatcher
from pynetest.lib.matchers.has_length_matcher import HasLengthMatcher
from pynetest.lib.matchers.matches_list_matcher import MatchesListMatcher


def equal_to(value):
    return EqualToMatcher(value)


def same_instance_as(value):
    return Matcher("same_instance_as", lambda a, b: a is b, value)


def is_none():
    return Matcher("is_none", lambda subject, *params: subject is None, None)


def anything():
    return Matcher("anything", lambda subject, *params: True)


def match(regular_expression):
    return Matcher("match", lambda subject, *params: re.search(params[0], subject), regular_expression)


def contains_text(text):
    return Matcher("contains_text", lambda subject, *params: isinstance(subject, str) and params[0] in subject, text)


def contains(item):
    def contains_comparator(subject, *params):
        if is_matcher(item):
            for candidate in subject:
                if item.matches(candidate):
                    return True
            return False
        else:
            try:
                return item in subject
            except TypeError:
                return False

    return Matcher("contains", contains_comparator, item)


def contained_in(collection):
    return Matcher("contained_in", lambda subject, *params: subject in params[0], collection)


def instance_of(clazz):
    if is_matcher(clazz):
        return Matcher("instance_of", lambda subject, *params: clazz.matches(subject.__class__), clazz)
    else:
        return Matcher("instance_of", lambda subject, *params: isinstance(subject, clazz), clazz)


def at_least(number):
    return Matcher("at_least", lambda subject, *params: subject >= number, number)


def at_most(number):
    return Matcher("at_most", lambda subject, *params: subject <= number, number)


def has_length(number):
    return HasLengthMatcher(number)

def between(lower, upper):
    return Matcher("between", lambda subject, *params: lower < subject < upper, lower, upper)


def about(number, tolerance=0.001):
    return Matcher("about", lambda subject, *params: -tolerance < number - subject < tolerance, number)


def matches_list(expected_list):
    return MatchesListMatcher(expected_list)
