from pynetest.expectations import expect
from pynetest.pyne_test_collector import it
from pynetest.pyne_tester import pyne


@pyne
def some_failing_file_test():
    @it("can fail")
    def _(self):
        expect(True).to_be(False)
