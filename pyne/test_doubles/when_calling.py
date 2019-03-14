from contextlib import ExitStack

from pyne.test_doubles.spy import Spy


def when_calling(method, on=None):
    if on is None and hasattr(method, '__self__'):
        object_to_stub = method.__self__
    else:
        object_to_stub = on
    spy = Spy(object_to_stub, method)
    return spy


class WhenCallingGroup(ExitStack):
    def __init__(self, *when_callings):
        ExitStack.__init__(self)
        self.when_callings = when_callings
        for when_calling in when_callings:
            self.enter_context(when_calling)

    def restore(self):
        for when_calling in self.when_callings:
            when_calling.restore()

def group_when_callings(*when_callings):
    return WhenCallingGroup(*when_callings)

when = when_calling
stub = when_calling
spy_on = when_calling
