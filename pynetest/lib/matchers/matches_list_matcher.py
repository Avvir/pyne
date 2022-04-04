from pynetest.lib.matcher import Matcher, equal_to_comparator


class MatchesListMatcher(Matcher):
    def __init__(self, expected_list):
        super().__init__("matches_list", self.list_comparator, expected_list)

    def list_comparator(self, subject, *params):
        expected = params[0]
        if subject is expected:
            if subject == ():
                return True
            else:
                self._reason = "it was the exact same instance"
                return False
        elif len(subject) == len(expected):
            for subject_item, expected_item in zip(subject, expected):
                if not equal_to_comparator(subject_item, expected_item):
                    return False
            return True
        else:
            return False

    def reason(self):
        return self._reason
