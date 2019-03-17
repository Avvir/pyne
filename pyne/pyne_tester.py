from pyne.pyne_config import config
from pyne.lib.result_reporters.pyne_result_reporters import reporter
from pyne.lib.pyne_test_blocks import DescribeBlock
from pyne.pyne_test_collector import test_collection
from pyne.pyne_test_runner import run_tests

class PyneBlock(DescribeBlock):
    def __init__(self, context_description, method):
        DescribeBlock.__init__(self, None, context_description, method)
        self.module_file = PyneBlock._current_module_file

    def __enter__(self):
        return DescribeBlock.__enter__(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        DescribeBlock.__exit__(self, exc_type, exc_val, exc_tb)


class PyneBlockModuleFile:
    def __init__(self, module_file):
        self.module_file = module_file

    def __enter__(self):
        PyneBlock._current_module_file = self.module_file

    def __exit__(self, exc_type, exc_val, exc_tb):
        PyneBlock._current_module_file = None


def pyne(tests_method):
    if config.report_between_suites:
        reporter.reset()
    describe_block = PyneBlock(tests_method.__name__, tests_method)
    test_collection.collect_describe(describe_block)
    if config.report_between_suites:
        run_tests(describe_block, reporter)
    return tests_method
