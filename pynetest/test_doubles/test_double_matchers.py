from pynetest.lib.matchers.was_called_with_matcher import WasCalledWithMatcher


def was_called_with(*expected_args, **expected_kwargs):
    return WasCalledWithMatcher((expected_args, expected_kwargs))
