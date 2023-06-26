from pynetest.lib.pyne_test_blocks import AfterEachBlock, BeforeEachBlock, DescribeBlock, ItBlock, BeforeFirstBlock


def no_tests():
    raise Exception("No tests to run.")


class PyneTestCollector:
    def __init__(self):
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


test_collection = PyneTestCollector()


def reset():
    test_collection.reset()


def it(method_or_description):
    if isinstance(method_or_description, str):
        description = method_or_description

        def named_it(method):
            test_collection.current_describe.it_blocks.append(
                    ItBlock(test_collection.current_describe, description, method))

        return named_it
    else:
        method = method_or_description
        test_collection.current_describe.it_blocks.append(
                ItBlock(test_collection.current_describe, method.__name__, method))
        return method_or_description


def fit(method_or_description):
    flag_ancestors_of_focus(test_collection.current_describe)

    if isinstance(method_or_description, str):
        description = method_or_description

        def named_focused_it(method):
            test_collection.current_describe.it_blocks.append(
                    ItBlock(test_collection.current_describe, description, method, focused=True))

        return named_focused_it
    else:
        method = method_or_description
        test_collection.current_describe.it_blocks.append(
                ItBlock(test_collection.current_describe, method.__name__, method, focused=True))
        return method_or_description


def xit(method_or_description):
    if isinstance(method_or_description, str):
        description = method_or_description

        def named_xit(method):
            test_collection.current_describe.it_blocks.append(
                    ItBlock(test_collection.current_describe, description, method, pending=True))

        return named_xit
    else:
        method = method_or_description
        test_collection.current_describe.it_blocks.append(
                ItBlock(test_collection.current_describe, method.__name__, method, pending=True))
        return method_or_description


def describe(method_or_description):
    if isinstance(method_or_description, str):
        description = method_or_description

        def named_describe(method):
            test_collection.current_describe.describe_blocks.append(
                    DescribeBlock(test_collection.current_describe, description, method))

        return named_describe
    else:
        method = method_or_description
        test_collection.current_describe.describe_blocks.append(
                DescribeBlock(test_collection.current_describe, method.__name__, method))
        return method_or_description


def xdescribe(method_or_description):
    if isinstance(method_or_description, str):
        description = method_or_description

        def named_describe(method):
            test_collection.current_describe.describe_blocks.append(
                    DescribeBlock(test_collection.current_describe, description, method, pending=True))

        return named_describe
    else:
        method = method_or_description
        test_collection.current_describe.describe_blocks.append(
                DescribeBlock(test_collection.current_describe, method.__name__, method, pending=True))
        return method_or_description


def fdescribe(description):
    flag_ancestors_of_focus(test_collection.current_describe)

    def named_focused_describe(method):
        test_collection.current_describe.describe_blocks.append(
                DescribeBlock(test_collection.current_describe, description, method, focused=True))

    return named_focused_describe


def before_each(method):
    test_collection.current_describe.before_each_blocks.append(
            BeforeEachBlock(test_collection.current_describe, method))
    return method


def before_first(method):
    test_collection.current_describe.before_first_blocks.append(
        BeforeFirstBlock(test_collection.current_describe, method))
    return method

def after_each(method):
    test_collection.current_describe.after_each_blocks.append(
            AfterEachBlock(test_collection.current_describe, method))
    return method


def flag_ancestors_of_focus(describe_block):
    if describe_block is not None and not describe_block.has_focused_descendants:
        describe_block.has_focused_descendants = True
        flag_ancestors_of_focus(describe_block.parent)
