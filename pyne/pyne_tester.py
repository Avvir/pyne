import inspect
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

def do_module_imports(module_importer):
    if module_importer is None:
        return
    module_path, module_name = module_importer.module_file
    import sys
    sys.path.index(0, module_path)
    module = __import__(module_name)
    sys.path.pop(0)
    return module

class PyneBlock(DescribeBlock, ModuleImportContext):
    _current_pyne_block_importer = None
    disable_pyne_decorator = False

    def __init__(self, context_description, method):
        DescribeBlock.__init__(self, None, context_description, method)
        ModuleImportContext.__init__(self)
        self.module_importer = PyneBlock._current_pyne_block_importer

    def __enter__(self):
        PyneBlock.disable_pyne_decorator = True
        do_module_imports(self.module_importer)
        ModuleImportContext.__enter__(self)
        return DescribeBlock.__enter__(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        DescribeBlock.__exit__(self, exc_type, exc_val, exc_tb)
        ModuleImportContext.__exit__(self, exc_type, exc_val, exc_tb)
        PyneBlock.disable_pyne_decorator = False


class PyneBlockImporter:
    def __init__(self, importer, module_directory, package_name):
        self.module_file = (module_directory, package_name)
        module = importer.find_module(package_name).load_module(package_name)
        members = dict(inspect.getmembers(module))
        members = { name: value for name, value in members.items() if not name.startswith("__") }
        self.members = { name: value for name, value in members.items() if not name.startswith("__") }

    def __enter__(self):
        PyneBlock._current_pyne_block_importer = self

    def __exit__(self, exc_type, exc_val, exc_tb):
        PyneBlock._current_pyne_block_importer = None


def pyne(tests_method):
    if PyneBlock.disable_pyne_decorator:
        return
    if config.report_between_suites:
        reporter.reset()
    describe_block = PyneBlock(tests_method.__name__, tests_method)
    test_collection.collect_describe(describe_block)
    if config.report_between_suites:
        run_tests(describe_block, reporter)
    return tests_method
