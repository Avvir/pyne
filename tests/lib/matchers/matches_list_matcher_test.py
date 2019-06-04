from pynetest.expectations import expect
from pynetest.lib.matchers.matches_list_matcher import MatchesListMatcher
from pynetest.matchers import about


def test__matches_list_matcher__can_match():
    expect([1, 2, 3, "banana"]).to_be(MatchesListMatcher([1, 2, 3, "banana"]))


def test__matches_list_matcher__when_lists_have_different_lengths__does_not_match():
    expect([1, 2, 3, 4]).not_to_be(MatchesListMatcher([1, 2, 3, 4, 4]))
    expect([1, 2, 3, 4, 4]).not_to_be(MatchesListMatcher([1, 2, 3, 4]))


def test__matches_list_matcher__when_lists_contain_different_items__does_not_match():
    expect([1, 2, "banana"]).not_to_be(MatchesListMatcher([1, 3, "banana"]))


def test__matches_list_matcher__when_list_is_the_same_instance__does_not_match():
    some_list = [1, 2, 3, 4]

    expect(some_list).not_to_be(MatchesListMatcher(some_list))


def test__matches_list_matcher__when_comparing_empty_tuples__matches():
    expect(()).to_be(MatchesListMatcher(()))


def test__matches_list_matcher__when_list_is_the_same_instance__explains_why_not():
    some_list = [1, 2, 3, 4]

    matcher = MatchesListMatcher(some_list)
    matcher.matches(some_list)
    expect(matcher.reason()).to_contain("it was the exact same instance")


def test__matches_list_matcher__supports_matchers_in_the_list():
    expect([1]).to_be(MatchesListMatcher([about(1)]))
