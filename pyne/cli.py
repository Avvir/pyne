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

from pyne.pyne_result_reporters import reporter
from pyne.pyne_test_collector import test_collection
from pyne.pyne_test_runner import run_tests
from pyne.pyne_config import config

click_completion.init()
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


class PyneCliHelper:
    def __init__(self):
        self.report_between_suites = False

    @staticmethod
    def load_all_tests_in_dir(dirname):
        for importer, package_name, _ in pkgutil.iter_modules([dirname]):
            if "_test" == package_name[-5:] and package_name not in sys.modules:
                module = importer.find_module(package_name
                                              ).load_module(package_name)
                print(module)

    def setup_reporting(self):
        self.report_between_suites = config.report_between_suites
        config.report_between_suites = False
        reporter.reset()
        test_collection.reset()


cli_helper = PyneCliHelper()


@group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@argument('path', required=False, type=Path(resolve_path=True), default=".")
@pass_context
def main(context, path):
    cli_helper.setup_reporting()

    cli_helper.load_all_tests_in_dir(path)

    for content in os.listdir(path):
        content_path = os.path.join(path, content)
        if os.path.isdir(content_path):
            cli_helper.load_all_tests_in_dir(content_path)

    describe_block = test_collection.top_level_describe
    run_tests(describe_block, reporter)

    config.report_between_suites = cli_helper.report_between_suites


if __name__ == "__main__":
    main()
