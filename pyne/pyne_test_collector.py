from pyne.pyne_config import config
from pyne.pyne_test_blocks import DescribeBlock, ItBlock, BeforeEachBlock


def reset():
    config.test_collection.reset()


def it(method_or_description):
    if isinstance(method_or_description, str):
        description = method_or_description

        def named_it(method):
            config.test_collection.current_describe.it_blocks.append(
                ItBlock(config.test_collection.current_describe, description, method))

        return named_it
    else:
        method = method_or_description
        config.test_collection.current_describe.it_blocks.append(
            ItBlock(config.test_collection.current_describe, method.__name__, method))


def xit(method_or_description):
    if isinstance(method_or_description, str):
        description = method_or_description

        def named_xit(method):
            config.test_collection.current_describe.it_blocks.append(
                ItBlock(config.test_collection.current_describe, description, method, pending=True))

        return named_xit
    else:
        method = method_or_description
        config.test_collection.current_describe.it_blocks.append(
            ItBlock(config.test_collection.current_describe, method.__name__, method, pending=True))


def describe(method_or_description):
    if isinstance(method_or_description, str):
        description = method_or_description

        def named_describe(method):
            config.test_collection.current_describe.describe_blocks.append(
                DescribeBlock(config.test_collection.current_describe, description, method))

        return named_describe
    else:
        method = method_or_description
        config.test_collection.current_describe.describe_blocks.append(
            DescribeBlock(config.test_collection.current_describe, method.__name__, method))


def xdescribe(method_or_description):
    if isinstance(method_or_description, str):
        description = method_or_description

        def named_describe(method):
            config.test_collection.current_describe.describe_blocks.append(
                DescribeBlock(config.test_collection.current_describe, description, method, pending=True))

        return named_describe
    else:
        method = method_or_description
        config.test_collection.current_describe.describe_blocks.append(
            DescribeBlock(config.test_collection.current_describe, method.__name__, method, pending=True))


def fdescribe(description):
    flag_ancestors_of_focus(config.test_collection.current_describe)

    def named_focused_describe(method):
        config.test_collection.current_describe.describe_blocks.append(
            DescribeBlock(config.test_collection.current_describe, description, method, focused=True))

    return named_focused_describe


def before_each(method):
    config.test_collection.current_describe.before_each_blocks.append(
        BeforeEachBlock(config.test_collection.current_describe, method))


def fit(method_or_description):
    flag_ancestors_of_focus(config.test_collection.current_describe)

    if isinstance(method_or_description, str):
        description = method_or_description

        def named_focused_it(method):
            config.test_collection.current_describe.it_blocks.append(
                ItBlock(config.test_collection.current_describe, description, method, focused=True))

        return named_focused_it
    else:
        method = method_or_description
        config.test_collection.current_describe.it_blocks.append(
            ItBlock(config.test_collection.current_describe, method.__name__, method, focused=True))


def flag_ancestors_of_focus(describe_block):
    if describe_block is not None and not describe_block.has_focused_descendants:
        describe_block.has_focused_descendants = True
        flag_ancestors_of_focus(describe_block.parent)
