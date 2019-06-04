from pynetest.pyne_test_collector import describe, it
from pynetest.pyne_tester import pyne


def run_failing_function():
    raise RuntimeError("PDB should come to me!")


@pyne
def fallback_to_pdb_test():
    @describe("When there is an error in a pyne test and the test is run via pdb")
    def _():
        @it("it follows the exception to the actual code pathway and not pyne")
        def _(self):
            import inspect
            frame_string = str(inspect.getouterframes(inspect.currentframe()))
            debug = "pydev" in frame_string
            if not debug:
                raise RuntimeError("Please run this test via PDB")
            run_failing_function()


