from pyne.lib.matchers.matches_list_matcher import MatchesListMatcher
from pyne.matchers import equal_to_comparator, Matcher


def was_called_with(*expected_args, **expected_kwargs):
    def was_called_comparator(subject, params):
        expected_call_args, expected_call_kwargs = params
        call_args, call_kwargs = subject.last_call

        matches_args = MatchesListMatcher(expected_call_args)
        return matches_args.list_comparator(call_args, expected_call_args) \
               and equal_to_comparator(call_kwargs, expected_call_kwargs)

    return Matcher("was_called_with", was_called_comparator, (expected_args, expected_kwargs))
