#!/usr/bin/env python
import os
import pkgutil
import sys

import click_completion
from click import (
    argument,
    group,
    pass_context,
    Path)

from pynetest.lib.result_reporters.pyne_result_reporters import reporter, TestFailureException
from pynetest.pyne_test_collector import test_collection
from pynetest.pyne_test_runner import run_tests
from pynetest.pyne_config import config

click_completion.init()
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


class PyneCliHelper:
    def __init__(self):
        self.report_between_suites = False

    @staticmethod
    def load_tests_in_dir(dirname, excluded_package_names):
        excluded_pyne_test_filename = os.path.join(dirname, "excluded_pyne_tests.txt")
        if os.path.exists(excluded_pyne_test_filename):
            with open(excluded_pyne_test_filename, "r") as fh:
                new_names = [n.strip() for n in fh.readlines()]
                for name in new_names:
                    excluded_package_names[name] = excluded_pyne_test_filename
        for importer, package_name, _ in sorted(list(pkgutil.iter_modules([dirname])), key=lambda x: x[1]):
            if "_test" == package_name[-5:] and package_name not in sys.modules:
                if package_name in excluded_package_names:
                    exclude_file = excluded_package_names[package_name]
                    print("Ignoring %s from exclude file %s" % (package_name, exclude_file))
                    continue
                module = importer.find_module(package_name
                                              ).load_module(package_name)
                print(module)

    @staticmethod
    def load_tests_in_subdirectories(path, excluded_package_names):
        for content in sorted(os.listdir(path)):
            if content[:1] != '.':
                content_path = os.path.join(path, content)
                if os.path.isdir(content_path):
                    cli_helper.load_tests_in_dir(content_path, excluded_package_names)
                    cli_helper.load_tests_in_subdirectories(content_path, excluded_package_names)

    def setup_reporting(self):
        self.report_between_suites = config.report_between_suites
        config.report_between_suites = False
        reporter.reset()
        test_collection.reset()


cli_helper = PyneCliHelper()


@group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@argument('paths', required=False, type=Path(resolve_path=True), nargs=-1)
@pass_context
def main(context, paths):
    if len(paths) == 0:
        paths = [os.path.realpath(".")]
    cli_helper.setup_reporting()
    excluded_package_names = dict()
    for path in paths:
        cli_helper.load_tests_in_dir(path, excluded_package_names)
        cli_helper.load_tests_in_subdirectories(path, excluded_package_names)

    describe_block = test_collection.top_level_describe
    try:
        run_tests(describe_block, reporter)
    except TestFailureException:
        sys.exit(1)

    config.report_between_suites = cli_helper.report_between_suites


if __name__ == "__main__":
    main()
