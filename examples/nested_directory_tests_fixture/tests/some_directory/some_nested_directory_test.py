from pynetest.pyne_test_collector import it, describe, before_each
from pynetest.pyne_tester import pyne


@pyne
def some_nested_directory_test():
    @describe("When setup fails")
    def _():
        @before_each
        def _(self):
            raise Exception("some test failure")

        @it("can fail")
        def _(self):
            pass

    @it("can also pass")
    def _(self):
        pass

    @it("can also pass")
    def _(self):
        pass
