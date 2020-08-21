from pynetest.lib.matcher import Matcher, equal_to_comparator


class HasLengthMatcher(Matcher):
    def __init__(self, number):
        Matcher.__init__(self, "has_length", self.comparator, number)

    def comparator(self, subject, number):
        matches = equal_to_comparator(len(subject), number)
        if not matches:
            self._reason = f"has length <{len(subject)}>"
        return matches
