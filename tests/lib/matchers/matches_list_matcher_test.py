from pyne.expectations import expect
from pyne.lib.matchers.matches_list_matcher import MatchesListMatcher


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
