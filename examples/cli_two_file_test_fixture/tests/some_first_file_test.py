from pynetest.pyne_test_collector import it
from pynetest.pyne_tester import pyne


@pyne
def some_first_file_test():
    @it("can pass")
    def _(self):
        pass
