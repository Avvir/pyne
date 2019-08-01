from pynetest.lib.matcher import Matcher
from pynetest.lib.message_format_helper import format_arguments
from pynetest.test_doubles.spy import Spy


class WasCalledMatcher(Matcher):
    def __init__(self):
        super().__init__("was_called", self.comparator)

    def comparator(self, subject):
        subject = Spy.get_spy(subject)
        if not hasattr(subject, 'last_call'):
            self._reason = "its calls were not tracked. Hint: use stub() to track its calls"
            return False
        elif subject.last_call is None:
            self._reason = "it was never called"
            return False
        else:
            return True

class WasNotCalledMatcher(Matcher):
    def __init__(self):
        super().__init__("was_called", self.comparator)

    def comparator(self, subject):
        subject = Spy.get_spy(subject)
        if not hasattr(subject, 'last_call'):
            self._reason = "its calls were not tracked. Hint: use stub() to track its calls"
            return False
        elif subject.last_call:
            self._reason = "it was called"
            return False
        else:
            return True
