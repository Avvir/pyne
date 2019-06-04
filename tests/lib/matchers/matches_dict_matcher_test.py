from pynetest.expectations import expect
from pynetest.lib.matchers.matches_dict_matcher import MatchesDictMatcher
from pynetest.matchers import about


def test__matches_dict_matcher__can_match():
    expect({"some-key": "some-value",
            "some-other-key": 1234}) \
        .to_be(MatchesDictMatcher({"some-key": "some-value",
                                   "some-other-key": 1234}))


def test__matches_dict_matcher__when_dicts_have_different_lengths__does_not_match():
    expect({"some-key": "some-value",
            "some-other-key": 1234}).not_to_be(MatchesDictMatcher({"some-key": "some-value"}))
    expect({"some-key": "some-value"}).not_to_be(MatchesDictMatcher({"some-key": "some-value",
                                                                     "some-other-key": 1234}))


def test__matches_dict_matcher__when_dicts_contain_different_values__does_not_match():
    expect({"some-key": "some-value"}).not_to_be(MatchesDictMatcher({"some-key": 1234}))


def test__matches_dict_matcher__when_dicts_contain_different_values__explains_why_not():
    matcher = MatchesDictMatcher({"some-key": about(3)})
    matcher.matches({"some-key": 1234})
    expect(matcher.reason()).to_contain("value for <'some-key'> was <1234> and did not match <about(3)>")


def test__matches_dict_matcher__when_dicts_have_different_keys__does_not_match():
    expect({"some-key": "some-value"}).not_to_be(MatchesDictMatcher({"some-other-key": "some-value"}))


def test__matches_dict_matcher__when_dict_is_the_same_instance__does_not_match():
    some_dict = {"some-key": "some-value"}

    expect(some_dict).not_to_be(MatchesDictMatcher(some_dict))


def test__matches_dict_matcher__when_dict_is_the_same_instance__explains_why_not():
    some_dict = {"some-key": "some-value"}

    matcher = MatchesDictMatcher(some_dict)
    matcher.matches(some_dict)
    expect(matcher.reason()).to_contain("it was the exact same instance")


def test__matches_dict_matcher__supports_matchers_in_the_dict_values():
    expect({"some-key": 1}).to_be(MatchesDictMatcher({"some-key": about(1)}))
