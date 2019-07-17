from pyne.expectations import expect
from pyne.pyne_test_collector import it
from pyne.pyne_tester import pyne


@pyne
def some_failing_file_test():
    @it("can fail")
    def _(self):
        expect(True).to_be(False)
