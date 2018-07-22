from os import path
from os.path import abspath

project_root = abspath(path.join(path.dirname(path.abspath(__file__)), "..", ".."))


cli_test_fixture_path = path.join(project_root, "examples", "cli_test_fixture")
pyne_path = path.join(project_root, "pyne")
