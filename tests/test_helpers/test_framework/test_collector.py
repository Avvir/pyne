from tests.test_helpers.test_framework.test_blocks import DescribeBlock, ItBlock, BeforeEachBlock


class TestCollector:
    def __init__(self):
        self.top_level_describe = DescribeBlock(None, None, None)
        self.current_describe = self.top_level_describe

    def collect_describe(self, describe_block):
        self.current_describe = describe_block
        describe_block.method()

        for describe_block in describe_block.describe_blocks:
            self.collect_describe(describe_block)


test_collector = TestCollector()


def it(method):
    test_collector.current_describe.it_blocks.append(
        ItBlock(test_collector.current_describe, method.__name__, method))


def describe(method):
    test_collector.current_describe.describe_blocks.append(
        DescribeBlock(test_collector.current_describe, method.__name__, method))


def before_each(method):
    test_collector.current_describe.before_each_blocks.append(
        BeforeEachBlock(test_collector.current_describe, method))