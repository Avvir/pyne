from pyne.pyne_test_collector import it, fit
from pyne.pyne_tester import pyne


@pyne
def sample_test():
    @fit("can be focused")
    def _(self):
        pass

    @fit("can be focused")
    def _(self):
        pass

    @it("can be ignored")
    def _(self):
        pass