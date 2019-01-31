from pyne.lib.expectation import Expectation
from pyne.lib.matcher import Matcher
from tests.test_helpers.expectation_helpers import expect_expectation_to_fail_with_message


def test__assert_expected__when_the_matcher_has_a_failure_reason__prints_the_failure_reason():
    class MatcherWithFailureReason(Matcher):
        def __init__(self):
            super().__init__("some_matcher", lambda subject, *params: False)

        def reason(self):
            return "it was not like that, yo"

    expectation = Expectation("to_meet_some_condition", MatcherWithFailureReason())

    expect_expectation_to_fail_with_message(lambda: expectation.assert_expected("some-subject"),
                                            "Expected <some-subject> to meet some condition"
                                            " but it was not like that, yo")


def test__assert_expected__when_the_matcher_takes_no_args__prints_the_failure_reason():
    class MatcherWithNoArgs(Matcher):
        def __init__(self):
            super().__init__("some_matcher", lambda subject, *params: False)

    expectation = Expectation("to_meet_some_condition", MatcherWithNoArgs())

    expect_expectation_to_fail_with_message(
        lambda: expectation.assert_expected("some-subject"),
        "Expected <some-subject> to meet some condition")


def test__assert_expected__when_the_matcher_takes_one_arg__prints_the_failure_reason():
    class MatcherWithNoArgs(Matcher):
        def __init__(self):
            super().__init__("some_matcher", lambda subject, *params: False)

    expectation = Expectation("to_meet_some_condition_of", MatcherWithNoArgs())

    expect_expectation_to_fail_with_message(
        lambda: expectation.assert_expected("some-subject", "being-some-cool-thing"),
        "Expected <some-subject> to meet some condition of <being-some-cool-thing>")


def test__assert_expected__when_the_matcher_takes_multiple_args__prints_the_failure_reason():
    expectation = Expectation("to_meet_some_conditions_of", Matcher("some_matcher", lambda subject, *params: False))

    expect_expectation_to_fail_with_message(
        lambda: expectation.assert_expected("some-subject", "first-arg", 222222, "third-arg"),
        "Expected <some-subject> to meet some conditions of <<first-arg>, <222222>, <third-arg>>")
