from contextlib import ExitStack

from pynetest.test_doubles.spy import Spy


def stub(method, on=None, method_name=None):
    if on is None and hasattr(method, '__self__'):
        object_to_stub = method.__self__
    else:
        object_to_stub = on
    spy = Spy(object_to_stub, method, method_name)
    return spy


class StubGroup(ExitStack):
    def __init__(self, *stubs):
        ExitStack.__init__(self)
        self.stubs = stubs
        for each_stub in stubs:
            self.enter_context(each_stub)

    def restore(self):
        for each_stub in self.stubs:
            each_stub.restore()


def group_stubs(*stubs):
    return StubGroup(*stubs)


when = stub
when_calling = stub
spy_on = stub
