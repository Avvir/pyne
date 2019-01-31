from pyne.lib.matcher import Matcher


def list_comparator(subject, *params):
    expected = params[0]
    if subject is expected:
        return False
    if len(subject) == len(expected):
        for subject_item, expected_item in zip(subject, expected):
            if subject_item != expected_item:
                return False
        return True
    else:
        return False


class MatchesListMatcher(Matcher):
    def __init__(self, expected_list):

        super().__init__("matches_list", list_comparator, expected_list)

