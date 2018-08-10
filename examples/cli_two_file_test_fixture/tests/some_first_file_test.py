from pyne.pyne_test_collector import it, fit
from pyne.pyne_tester import pyne


@pyne
def some_first_file_test():
    @it("can pass")
    def _(self):
        pass
