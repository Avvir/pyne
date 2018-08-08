from pyne.pyne_test_collector import it
from pyne.pyne_tester import pyne


@pyne
def another_sample_test():
    @it("has some behavior in file 2")
    def _(self):
        pass

    @it("has some behavior in file 2")
    def _(self):
        pass
