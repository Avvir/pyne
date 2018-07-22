# import shutil
# import os
# from os import path
#
# import pytest
# from click.testing import CliRunner
# from pyne import cli
# from pyne.expectations import expect
# from tests.test_helpers.test_resource_paths import cli_test_fixture_path, pyne_path
#
#
# @pytest.fixture
# def runner():
#     return CliRunner()
#
#
# def copy_to_working_directory(resource_path):
#     if os.path.isdir(resource_path):
#         shutil.copytree(resource_path,
#                         path.abspath(path.join(path.curdir, path.basename(resource_path))))
#     else:
#         shutil.copy2(resource_path, path.abspath(path.join(path.curdir, path.basename(resource_path))))
#
#
# def test__when_there_is_a_tests_directory_with_a_test_file__runs_the_test(runner):
#     with runner.isolated_filesystem():
#         copy_to_working_directory(path.join(cli_test_fixture_path, 'tests'))
#         copy_to_working_directory(path.join(cli_test_fixture_path, 'pyne_config.json'))
#         copy_to_working_directory(pyne_path)
#
#         result = runner.invoke(cli.main)
#         expect(result.output).to_contain("1 passed")
