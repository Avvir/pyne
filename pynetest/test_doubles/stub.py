from contextlib import ExitStack

from pynetest.test_doubles.spy import Spy


def stub(method, on=None):
    if on is None and hasattr(method, '__self__'):
        object_to_stub = method.__self__
    else:
        object_to_stub = on

    spy = Spy(object_to_stub, method)
    return spy


class MegaStub(ExitStack):
    def __init__(self, *stubs):
        ExitStack.__init__(self)
        self.stubs = stubs

    def __enter__(self):
        for each_stub in self.stubs:
            self.enter_context(each_stub)

    def stub(self):
        for each_stub in self.stubs:
            each_stub.stub()

    def unstub(self):
        for each_stub in self.stubs:
            each_stub.unstub()

    def restore(self):
        for each_stub in self.stubs:
            each_stub.restore()



class StubGroup(ExitStack):
    def __init__(self, *stubs):
        ExitStack.__init__(self)
        self.stubs = stubs
        for each_stub in stubs:
            self.enter_context(each_stub)

    def restore(self):
        for each_stub in self.stubs:
            each_stub.restore()

def mega_stub(*stubs):
    return MegaStub(*stubs)

def group_stubs(*stubs):
    import warnings
    warnings.warn("group_stubs / StubGroup is deprecated and will be removed soon. Please use mega_stub / MegaStub instead", DeprecationWarning)
    print("DEPRECATED WARNING: group_stubs / StubGroup is deprecated and will be removed soon. Please use mega_stub / MegaStub instead", DeprecationWarning)
    return StubGroup(*stubs)


when = stub
when_calling = stub
spy_on = stub
