#!/usr/bin/env python
import os

import click_completion
from click import (
    argument,
    group,
    pass_context,
    Path)

from pyne.cli_helper import cli_helper
from pyne.pyne_result_reporters import reporter
from pyne.pyne_test_runner import run_tests

click_completion.init()
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


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

    describe_block = cli_helper.config.test_collection.top_level_describe
    run_tests(describe_block, reporter)

    cli_helper.config.report_between_suites = cli_helper.report_between_suites


if __name__ == "__main__":
    main()
