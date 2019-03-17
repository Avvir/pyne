import sys

from pyne.pyne_config import config
from pyne.lib.result_reporters.pyne_result_reporters import reporter
from pyne.lib.pyne_test_blocks import DescribeBlock
from pyne.pyne_test_collector import test_collection
from pyne.pyne_test_runner import run_tests

class ModuleImportContext:
    def __init__(self):
        self.enter_module_names = None

    def __enter__(self):
        self.enter_module_names = set(sys.modules.keys())

    def __exit__(self, exc_type, exc_val, exc_tb):
        exit_module_names = sys.modules.keys()
        added_module_names = exit_module_names - self.enter_module_names
        for module_name in added_module_names:
            print("Removing", module_name)
            sys.modules.pop(module_name)

def load_module_file(module_file):
    if module_file is None:
        return
    module_path, module_name = module_file
    import sys
    sys.path.index(0, module_path)
    module = __import__(module_name)
    sys.path.pop(0)
    return module

class PyneBlock(DescribeBlock, ModuleImportContext):
    _current_module_file = None
    def __init__(self, context_description, method):
        DescribeBlock.__init__(self, None, context_description, method)
        # ModuleImportContext.__init__(self)
        self.module_file = PyneBlock._current_module_file

    def __enter__(self):
        # load_module_file(self.module_file)
        # ModuleImportContext.__enter__(self)
        return DescribeBlock.__enter__(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        DescribeBlock.__exit__(self, exc_type, exc_val, exc_tb)
        # ModuleImportContext.__exit__(self, exc_type, exc_val, exc_tb)


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
