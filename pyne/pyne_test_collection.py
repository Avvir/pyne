def no_tests():
    raise Exception("No tests to run.")


class PyneTestCollection:
    def __init__(self):
        from pyne.pyne_test_blocks import DescribeBlock
        self.top_level_describe = DescribeBlock(None, "All Tests", no_tests)
        self.current_describe = self.top_level_describe

    def collect_describe(self, describe_block):
        if describe_block.parent is None:
            self.top_level_describe.describe_blocks.append(describe_block)
            describe_block.parent = self.top_level_describe
        self.current_describe = describe_block
        describe_block.method()

        for describe_block in describe_block.describe_blocks:
            self.collect_describe(describe_block)

    def reset(self):
        self.top_level_describe = DescribeBlock(None, "All Tests", no_tests)
        self.current_describe = self.top_level_describe
