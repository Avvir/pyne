from tests.test_helpers.test_framework.test_blocks import DescribeBlock
from tests.test_helpers.test_framework.test_collector import test_collection
from tests.test_helpers.test_framework.test_runner import run_tests


def pyne(tests_method):
    describe_block = DescribeBlock(None, tests_method.__name__, tests_method)
    test_collection.collect_describe(describe_block)
    run_tests(describe_block)
