from pyne.pyne_test_collector import it
from pyne.pyne_tester import pyne


@pyne
def run_included_e_test():
    @it("can pass")
    def _(self):
        pass
