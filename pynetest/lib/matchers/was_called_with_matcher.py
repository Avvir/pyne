from pynetest.lib.matcher import Matcher
from pynetest.lib.matchers.matches_dict_matcher import MatchesDictMatcher
from pynetest.lib.matchers.matches_list_matcher import MatchesListMatcher
from pynetest.lib.matchers.was_called_matcher import WasCalledMatcher
from pynetest.lib.message_format_helper import format_arguments
from pynetest.test_doubles.spy import Spy, last_call_of


def _get_named_positional_arg_count(signature):
    if not signature:
        0
    for i, (name, param_def) in enumerate(signature.parameters.items()):
        if param_def.kind not in [param_def.POSITIONAL_ONLY, param_def.POSITIONAL_OR_KEYWORD]:
            return i
    return len(signature.parameters.items()) - 1


def _get_varargs(signature, args):
    if not signature:
        return args
    named_positional_arg_count = _get_named_positional_arg_count(signature)
    if named_positional_arg_count >= len(args):
        return []
    else:
        return args[named_positional_arg_count:]


def _get_all_named_args(signature, args, kwargs):
    if not signature:
        return kwargs
    named_positional_arg_count = _get_named_positional_arg_count(signature)
    all_named_args = dict(kwargs)

    for i in range(0, min(named_positional_arg_count, len(args))):
        name, param_def = list(signature.parameters.items())[i]
        all_named_args[name] = args[i]

    return all_named_args


class WasCalledWithMatcher(Matcher):
    def __init__(self, *params):
        super().__init__("was_called_with", self.comparator, *params)

    def comparator(self, subject, params):
        was_called_matcher = WasCalledMatcher()
        if not was_called_matcher.matches(subject):
            self._reason = was_called_matcher.reason()
            return False
        subject = Spy.get_spy(subject)
        expected_call_args, expected_call_kwargs = params

        call_args, call_kwargs = subject.last_call

        expected_named_args = _get_all_named_args(subject.signature, expected_call_args, expected_call_kwargs)
        actual_named_args = _get_all_named_args(subject.signature, call_args, call_kwargs)

        expected_varargs = _get_varargs(subject.signature, expected_call_args)
        actual_varargs = _get_varargs(subject.signature, call_args)

        matches_varargs = MatchesListMatcher(expected_varargs)
        matches_named_args = MatchesDictMatcher(expected_named_args)
        self._reason = "it was called with <" + format_arguments(call_args, call_kwargs) + ">"
        return matches_varargs.list_comparator(actual_varargs, expected_varargs) and \
               matches_named_args.comparator(actual_named_args, expected_named_args)
