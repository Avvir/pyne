import shutil
import os
from os import path

from click.testing import CliRunner
from pynetest import cli
from pynetest.expectations import expect
from pynetest.pyne_config import config
from tests.test_helpers.test_resource_paths import cli_test_fixture_path, pyne_path, cli_two_file_test_fixture_path, \
    cli_focused_test_fixture_path, cli_nested_directory_tests_fixture_path, cli_hidden_file_path, \
    cli_excluded_tests_fixture_path, cli_failing_tests_fixture_path


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


def test__when_there_are_nested_directories_of_test_files__summarizes_the_results_together():
    runner = CliRunner()
    with runner.isolated_filesystem():
        copy_to_working_directory(path.join(cli_nested_directory_tests_fixture_path, 'tests'))
        copy_to_working_directory(pyne_path)

        result = runner.invoke(cli.main)
        expect(result.output).to_contain("some_top_directory_test")
        expect(result.output).to_contain("some_nested_directory_test")
        expect(result.output).to_contain("1 failed, 3 passed")
        expect(result.output).to_contain("All Tests >> some_nested_directory_test >> When setup fails >> can fail")


def test_when_there_is_a_hidden_subdirectory__does_not_look_for_tests():
    runner = CliRunner()
    with runner.isolated_filesystem():
        copy_to_working_directory(path.join(cli_hidden_file_path, '.hidden_dir'))
        copy_to_working_directory(pyne_path)

        result = runner.invoke(cli.main)
        expect(result.output).to_contain("Ran 0 tests")


def test_when_there_is_a_list_of_excluded_tests__does_not_run_them():
    runner = CliRunner()
    with runner.isolated_filesystem():
        copy_to_working_directory(path.join(cli_excluded_tests_fixture_path, 'tests'))
        copy_to_working_directory(pyne_path)
        result = runner.invoke(cli.main)
        expect(result.output).not_to_contain("run_excluded_a_test")
        expect(result.output).not_to_contain("run_excluded_b_test")
        expect(result.output).to_contain("run_included_c_test")
        expect(result.output).to_contain("run_included_d_test")
        expect(result.output).to_contain("run_included_e_test")
        # import time
        # time.sleep(50000)


def test_when_there_is_a_failing_test__does_exits_with_code_1():
    runner = CliRunner()
    with runner.isolated_filesystem():
        copy_to_working_directory(path.join(cli_failing_tests_fixture_path, 'tests'))
        copy_to_working_directory(pyne_path)
        result = runner.invoke(cli.main)
        expect(result.exit_code).to_be(1)
        expect(result.exception).to_be_a(SystemExit)


def test_cleanup():
    config.report_between_suites = True
