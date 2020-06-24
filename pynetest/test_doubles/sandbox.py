from pynetest.test_doubles.stub import stub


class Sandbox:
    def __init__(self):
        self._spies = []

    def spy(self, object_to_stub=None, method=None):
        new_spy = stub(object_to_stub, method)
        self._spies.append(new_spy)
        return new_spy

    def when_calling(self, object_to_stub=None, method=None):
        return self.spy(object_to_stub, method)

    def restore(self):
        for spy in self._spies:
            spy.restore()
        self._spies = []

    def reset(self):
        for spy in self._spies:
            spy.reset()
