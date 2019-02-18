from pyne.lib.matcher import Matcher, equal_to_comparator


class MatchesDictMatcher(Matcher):
    def __init__(self, expected_list):
        super().__init__("matches_list", self.comparator, expected_list)

    def comparator(self, subject, *params):
        expected = params[0]
        if subject is expected:
            self._reason = "it was the exact same instance"
            return False
        elif len(subject) == len(expected):
            for i, (expected_key, expected_value) in enumerate(expected.items()):
                if expected_key in subject:
                    subject_item_value = subject[expected_key]
                    if not equal_to_comparator(subject_item_value, expected_value):
                        return False
                else:
                    self._reason = "subject did not have the key <" + str(expected_key) + ">"
                    return False
            return True
        else:
            return False

    def reason(self):
        return self._reason
