import shutil
import os
from os import path

# import pytest
from click.testing import CliRunner
from pyne import cli
from pyne.expectations import expect
from tests.test_helpers.test_resource_paths import cli_test_fixture_path, pyne_path, cli_two_file_test_fixture_path, \
    cli_focused_test_fixture_path


def copy_to_working_directory(resource_path):
    if os.path.isdir(resource_path):
        shutil.copytree(resource_path,
                        path.abspath(path.join(path.curdir, path.basename(resource_path))))
    else:
        shutil.copy2(resource_path, path.abspath(path.join(path.curdir)))


def test__when_there_is_a_tests_directory_with_a_test_file__runs_the_test():
    runner = CliRunner()
    with runner.isolated_filesystem():
        copy_to_working_directory(path.join(cli_test_fixture_path, 'tests'))
        copy_to_working_directory(pyne_path)

        result = runner.invoke(cli.main)

        expect(result.output).to_contain("some_single_test")
        expect(result.output).to_contain("1 passed")


def test__when_there_are_focused_tests__runs_only_those_tests():
    runner = CliRunner()
    with runner.isolated_filesystem():
        copy_to_working_directory(path.join(cli_focused_test_fixture_path, 'tests'))
        copy_to_working_directory(pyne_path)

        result = runner.invoke(cli.main)
        expect(result.output).to_contain("can be focused")
        expect(result.output).to_contain("4 passed")


def test__when_there_are_two_test_files__summarizes_the_results_together():
    runner = CliRunner()
    with runner.isolated_filesystem():
        copy_to_working_directory(path.join(cli_two_file_test_fixture_path, 'tests'))
        copy_to_working_directory(pyne_path)

        result = runner.invoke(cli.main)
        expect(result.output).to_contain("some_first_file_test")
        expect(result.output).to_contain("some_second_file_test")
        expect(result.output).to_contain("2 passed")
