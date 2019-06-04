from os import path
from os.path import abspath

project_root = abspath(path.join(path.dirname(path.abspath(__file__)), "..", ".."))


cli_test_fixture_path = path.join(project_root, "examples", "cli_single_test_fixture")
cli_two_file_test_fixture_path = path.join(project_root, "examples", "cli_two_file_test_fixture")
cli_nested_directory_tests_fixture_path = path.join(project_root, "examples", "nested_directory_tests_fixture")
cli_focused_test_fixture_path = path.join(project_root, "examples", "cli_focused_test_fixture")
cli_excluded_tests_fixture_path = path.join(project_root, "examples", "cli_excluded_tests_fixture")
cli_hidden_file_path = path.join(project_root, "examples", "cli_hidden_file_test_fixture")
cli_failing_tests_fixture_path = path.join(project_root, "examples", "cli_failing_tests_fixture")
pyne_path = path.join(project_root, "pynetest")
