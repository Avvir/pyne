from pynetest.pyne_test_collector import it
from pynetest.pyne_tester import pyne


@pyne
def some_top_directory_test():
    @it("can pass")
    def _(self):
        pass
