from pynetest.expectations import expect
from pynetest.pyne_test_collector import it, describe
from pynetest.pyne_tester import pyne
from foo import bar


@pyne
def some_failing_import_test():
    @describe("When there's a bad import")
    def _():
        @it("can fail")
        def _(self):
            expect(True).to_be(True)
