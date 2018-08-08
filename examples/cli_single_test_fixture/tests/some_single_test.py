from pyne.pyne_test_collector import it
from pyne.pyne_tester import pyne


@pyne
def sample_test():
    @it("has some behavior")
    def _(self):
        pass
