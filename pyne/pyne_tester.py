import inspect
import sys
from importlib import reload
from types import ModuleType

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


class PyneBlock(DescribeBlock, ModuleImportContext):
    collect_immediately = True

    def __init__(self, context_description, method, suite_name=None):
        DescribeBlock.__init__(self, None, context_description, method)
        ModuleImportContext.__init__(self)
        module_members = dict(method.__globals__)
        self.module_name = None
        self.module_directory = None
        self.module_members = { name: value for name, value in module_members.items() if not name.startswith("__") }
        self.module_name = method.__module__
        self.is_run_in_main = (method.__module__ == "__main__")
        self.suite_name = suite_name

    def __enter__(self):
        ModuleImportContext.__enter__(self)
        self.restore_module_members()
        return DescribeBlock.__enter__(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        DescribeBlock.__exit__(self, exc_type, exc_val, exc_tb)
        ModuleImportContext.__exit__(self, exc_type, exc_val, exc_tb)

    def restore_module_members(self):
        globals = self.method.__globals__
        for name, member in self.module_members.items():
            if isinstance(member, ModuleType):
                if member.__name__ not in sys.modules:
                    sys.modules[member.__name__] = member.__loader__.load_module()

    def collect(self):
        if config.report_between_suites:
            reporter.reset()
        test_collection.collect_describe(self)
        if config.report_between_suites:
            run_tests(self, reporter)

class DisablePyneBlockCollectImmediately:
    def __enter__(self):
        PyneBlock.collect_immediately = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        PyneBlock.collect_immediately = True

def suite(pyne_block, suite_name):
    pyne_block.suite_name = suite_name
    return pyne_block

def pyne(tests_method):
    pyne_block = PyneBlock(tests_method.__name__, tests_method)
    if PyneBlock.collect_immediately:
        pyne_block.collect()
    return pyne_block
