from distributed.client import Client
from pynetest.pyne_test_collector import it, describe
from pynetest.pyne_tester import pyne


@pyne
def multiprocessing_test():
    @describe("when a multiprocessing loop is created")
    def _():
        @it('only runs the tests once')
        def _(self):
            #when this is not working, this file will fail with an infinite loop
            with Client() as client:
                pass
