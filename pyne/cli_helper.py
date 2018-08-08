import pkgutil
import sys

from pyne.pyne_config import config
from pyne.pyne_result_reporters import reporter


class PyneCliHelper:
    def __init__(self):
        self.report_between_suites = False
        self.config = config

    @staticmethod
    def load_all_tests_in_dir(dirname):
        for importer, package_name, _ in pkgutil.iter_modules([dirname]):
            if "_test" == package_name[-5:] and package_name not in sys.modules:
                module = importer.find_module(package_name
                                              ).load_module(package_name)
                print(module)

    def setup_reporting(self):
        self.report_between_suites = self.config.report_between_suites
        self.config.report_between_suites = False
        reporter.reset()

cli_helper = PyneCliHelper()
