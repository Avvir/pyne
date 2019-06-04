from pynetest.pyne_test_collector import it
from pynetest.pyne_tester import pyne


@pyne
def some_second_file_test():
    @it("can also pass")
    def _(self):
        pass
