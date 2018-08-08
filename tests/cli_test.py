import io
import shutil
import os
import sys
from os import path

from click.testing import CliRunner
from pyne import cli
from pyne.expectations import expect
from pyne.matchers import contains
from pyne.pyne_config import config
from pyne.pyne_test_collection import PyneTestCollection
from pyne.pyne_test_collector import it, describe, fit, before_each
from pyne.pyne_tester import pyne
from tests.test_helpers.test_resource_paths import cli_test_fixture_path, pyne_path, cli_two_file_test_fixture_path, \
    cli_focused_test_fixture_path


def copy_to_working_directory(resource_path):
    if os.path.isdir(resource_path):
        shutil.copytree(resource_path,
                        path.abspath(path.join(path.curdir, path.basename(resource_path))))
    else:
        shutil.copy2(resource_path, path.abspath(path.join(path.curdir)))


# def d(result):
#     return result.output_bytes.decode('utf-8', 'replace') \
#         .replace('\r\n', '\n')
#
#
# def db(byte_output):
#     return byte_output.getvalue().decode('utf-8', 'replace') \
#         .replace('\r\n', '\n')
#
#
# def test__when_there_is_a_focused_test__runs_only_that_test():
#     runner = CliRunner()
#     with runner.isolated_filesystem():
#         # bytes_output = io.BytesIO()
#         # sys.stdout = sys.stderr = io.TextIOWrapper(
#         #     bytes_output, encoding='utf-8')
#
#         copy_to_working_directory(path.join(cli_focused_test_fixture_path, 'tests'))
#         copy_to_working_directory(pyne_path)
#
#         result = runner.invoke(cli.main)
#         expect(result.output).to_contain("can be focused")
#         expect(result.output).to_contain("4 passed")
#
#

#
# def test__when_there_is_a_tests_directory_with_a_test_file__runs_the_test():
#     runner = CliRunner()
#     with runner.isolated_filesystem():
#         with StubPrint():
#             copy_to_working_directory(path.join(cli_test_fixture_path, 'tests'))
#             copy_to_working_directory(pyne_path)
#
#             result = runner.invoke(cli.main)
#             expect(printed_text).to_contain(contains("1 passed"))
#

@pyne
def cli_test():
    @before_each
    def _(self):
        config.test_collection = PyneTestCollection()

    @describe("when there is a test file with a test in it")
    def _():
        @it("runs the test in the file")
        def _(self):

            runner = CliRunner()
            with runner.isolated_filesystem():
                copy_to_working_directory(path.join(cli_test_fixture_path, 'tests'))
                copy_to_working_directory(pyne_path)

                result = runner.invoke(cli.main)
                expect(result.output).to_contain("has some behavior")
                expect(result.output).to_contain("1 passed")

    @describe("when there is a focused test")
    def _():
        @it("runs only the focused test")
        def _(self):
            runner = CliRunner()
            with runner.isolated_filesystem():
                copy_to_working_directory(path.join(cli_focused_test_fixture_path, 'tests'))
                copy_to_working_directory(pyne_path)

                result = runner.invoke(cli.main)
                expect(result.output).to_contain("can be focused")
                expect(result.output).to_contain("4 passed")

    @describe("when there are two test files")
    def _():
        @it("summarizes the results together")
        def _(self):
            runner = CliRunner()
            with runner.isolated_filesystem():
                copy_to_working_directory(path.join(cli_two_file_test_fixture_path, 'tests'))
                copy_to_working_directory(pyne_path)

                result = runner.invoke(cli.main)
                expect(result.output).to_contain("has some behavior in file 1")
                expect(result.output).to_contain("has some behavior in file 2")
                expect(result.output).to_contain("3 passed")
