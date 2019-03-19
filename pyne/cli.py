#!/usr/bin/env python
import inspect
import os
import pkgutil
import sys

import click_completion
from click import (
    argument,
    group,
    pass_context,
    Path)

from pyne.lib.result_reporters.pyne_result_reporters import reporter
from pyne.pyne_test_collector import test_collection
from pyne.pyne_test_runner import run_tests
from pyne.pyne_config import config
from pyne.pyne_tester import ModuleImportContext, PyneBlock, DisablePyneBlockCollectImmediately

click_completion.init()
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])



class PyneCliHelper:
    def __init__(self):
        self.report_between_suites = False

    @staticmethod
    def load_tests_in_dir(module_directory):
        pyne_blocks = []
        excluded_module_names = dict()
        with DisablePyneBlockCollectImmediately():
            with ModuleImportContext():
                excluded_pyne_test_filename = os.path.join(module_directory, "excluded_pyne_tests.txt")
                if os.path.exists(excluded_pyne_test_filename):
                    with open(excluded_pyne_test_filename, "r") as fh:
                        new_names = [n.strip() for n in fh.readlines()]
                        for name in new_names:
                            excluded_module_names[name] = excluded_pyne_test_filename

                for importer, module_name, _ in pkgutil.iter_modules([module_directory]):
                    if "_test" == module_name[-5:] and module_name not in sys.modules:
                        module = importer.find_module(module_name).load_module(module_name)
                        for name, member in inspect.getmembers(module):
                            if isinstance(member, PyneBlock):
                                member.module_name = module_name
                                member.module_directory = module_directory
                                pyne_blocks.append(member)
        return pyne_blocks, excluded_module_names

    @staticmethod
    def load_tests_in_subdirectories(path):
        pyne_blocks = []
        excluded_module_names = dict()
        for content in os.listdir(path):
            if content[:1] != '.':
                content_path = os.path.join(path, content)
                if os.path.isdir(content_path):
                    blocks, excluded = cli_helper.load_tests_in_dir(content_path)
                    pyne_blocks.extend(blocks)
                    excluded_module_names.update(excluded)
                    blocks, excluded = cli_helper.load_tests_in_subdirectories(content_path)
                    pyne_blocks.extend(blocks)
                    excluded_module_names.update(excluded)
        return pyne_blocks, excluded_module_names

    @staticmethod
    def load_tests(path):
        ex = dict()
        pyne_blocks, excluded_module_names = cli_helper.load_tests_in_dir(path)
        blocks, excluded = cli_helper.load_tests_in_subdirectories(path)
        pyne_blocks.extend(blocks)
        excluded_module_names.update(excluded)
        return pyne_blocks, excluded_module_names

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
    pyne_blocks, excluded_module_names = cli_helper.load_tests(path)

    for pyne_block in pyne_blocks:
        if pyne_block.module_name in excluded_module_names:
            exclude_file = excluded_module_names[pyne_block.module_name]
            print("Ignoring %s from exclude file %s" % (pyne_block.module_name, exclude_file))
            continue
        pyne_block.collect()

    describe_block = test_collection.top_level_describe
    run_tests(describe_block, reporter)

    config.report_between_suites = cli_helper.report_between_suites


if __name__ == "__main__":
    main()
