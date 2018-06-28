from tests.test_helpers.test_framework.test_blocks import DescribeBlock
from tests.test_helpers.test_framework.test_collector import test_collection, it, describe, before_each
from tests.test_helpers.test_framework.expectations import expect


def test__it__adds_it_block_to_current_describe():
    current_describe = DescribeBlock(None, None, None)
    test_collection.current_describe = current_describe

    def some_method():
        pass

    it(some_method)
    expect(current_describe.it_blocks).to_have_length(1)
    expect(current_describe.it_blocks[0].method).to_be(some_method)


def test__describe__adds_describe_block_to_current_describe():
    current_describe = DescribeBlock(None, None, None)
    test_collection.current_describe = current_describe

    def some_method():
        pass

    describe(some_method)
    expect(current_describe.describe_blocks).to_have_length(1)
    expect(current_describe.describe_blocks[0].method).to_be(some_method)


def test__before_each__adds_before_each_block_to_current_describe():
    current_describe = DescribeBlock(None, None, None)
    test_collection.current_describe = current_describe

    def some_method():
        pass

    before_each(some_method)
    expect(current_describe.before_each_blocks).to_have_length(1)
    expect(current_describe.before_each_blocks[0].method).to_be(some_method)


def test__collect_describe__adds_children_to_the_describe():
    def describe_block_method():
        @describe
        def when_something_happens():
            pass

        @it
        def does_something():
            pass

        @before_each
        def do():
            pass
    describe_block = DescribeBlock(None, None, describe_block_method)

    test_collection.collect_describe(describe_block)

    expect(describe_block.before_each_blocks).to_have_length(1)
    expect(describe_block.describe_blocks).to_have_length(1)
    expect(describe_block.it_blocks).to_have_length(1)


def test__collect_describe__when_there_are_nested_describes__collects_them():
    def describe_block_method():
        @describe
        def when_something_happens():
            @before_each
            def do():
                pass

            @it
            def does_something():
                pass

            @describe
            def when_something_is_true():
                pass
    describe_block = DescribeBlock(None, None, describe_block_method)

    test_collection.collect_describe(describe_block)

    expect(describe_block.describe_blocks[0].before_each_blocks).to_have_length(1)
    expect(describe_block.describe_blocks[0].describe_blocks).to_have_length(1)
    expect(describe_block.describe_blocks[0].it_blocks).to_have_length(1)



