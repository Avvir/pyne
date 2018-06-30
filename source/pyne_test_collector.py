from source.pyne_test_blocks import DescribeBlock, ItBlock, BeforeEachBlock

def no_tests():
    raise Exception("No tests to run.")

class PyneTestCollector:
    def __init__(self):
        self.top_level_describe = DescribeBlock(None, None, no_tests)
        self.current_describe = self.top_level_describe

    def collect_describe(self, describe_block):
        self.current_describe = describe_block
        describe_block.method()

        for describe_block in describe_block.describe_blocks:
            self.collect_describe(describe_block)

    def reset(self):
        self.top_level_describe = DescribeBlock(None, None, no_tests)
        self.current_describe = self.top_level_describe


test_collection = PyneTestCollector()


def reset():
    test_collection.reset()


def it(method):
    test_collection.current_describe.it_blocks.append(
        ItBlock(test_collection.current_describe, method.__name__, method))


def describe(method):
    test_collection.current_describe.describe_blocks.append(
        DescribeBlock(test_collection.current_describe, method.__name__, method))


def before_each(method):
    test_collection.current_describe.before_each_blocks.append(
        BeforeEachBlock(test_collection.current_describe, method))
