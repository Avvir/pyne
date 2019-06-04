from pynetest.pyne_test_collector import it
from pynetest.pyne_tester import pyne


@pyne
def sample_test():
    @it("can pass")
    def _(self):
        pass
