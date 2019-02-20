from pyne.lib.matcher import Matcher


class WasCalledMatcher(Matcher):
    def __init__(self):
        super().__init__("was_called", self.comparator)

    def comparator(self, subject):
        if subject.last_call is None:
            self._reason = "it was never called"
            return False
        else:
            return True