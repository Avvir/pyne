from pynetest.pyne_config import config
from pynetest.lib.result_reporters.pyne_result_reporters import reporter, TestFailureException
from pynetest.lib.pyne_test_blocks import DescribeBlock
from pynetest.pyne_test_collector import test_collection
from pynetest.pyne_test_runner import run_tests


def replace_excepthook():
    import sys
    original_excepthook = sys.excepthook
    def new_excepthook(type, value, traceback):
        if type == TestFailureException:
            print(value)
            return
        else:
            original_excepthook(type, value, traceback)
    sys.excepthook = new_excepthook

def pyne(tests_method):
    if config.report_between_suites:
        reporter.reset()
    describe_block = DescribeBlock(None, tests_method.__name__, tests_method)
    test_collection.collect_describe(describe_block)
    if config.report_between_suites:
        run_tests(describe_block, reporter)
    return tests_method

replace_excepthook()
