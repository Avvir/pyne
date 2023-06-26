from pynetest.lib.pyne_test_blocks import DescribeBlock
from pynetest.pyne_test_collector import test_collection, it, describe, before_each, fit, fdescribe, after_each, before_first
from pynetest.expectations import expect


def test__it__adds_it_block_to_current_describe():
    current_describe = DescribeBlock(None, None, None)
    test_collection.current_describe = current_describe

    def some_method():
        pass

    it(some_method)
    expect(current_describe.it_blocks).to_have_length(1)
    expect(current_describe.it_blocks[0].method).to_be(some_method)


def test__it__when_using_string_description__adds_it_block_to_describe():
    current_describe = DescribeBlock(None, None, None)
    test_collection.current_describe = current_describe

    def some_method():
        pass

    it("some it name")(some_method)

    expect(current_describe.it_blocks).to_have_length(1)
    expect(current_describe.it_blocks[0].method).to_be(some_method)


def test__it__when_using_string_description__sets_the_description():
    current_describe = DescribeBlock(None, None, None)
    test_collection.current_describe = current_describe

    def some_method():
        pass

    it("some cool thing happens")(some_method)

    expect(current_describe.it_blocks[0].description).to_be("some cool thing happens")


def test__fit__adds_an_it_block_to_current_describe():
    current_describe = DescribeBlock(None, None, None)
    test_collection.current_describe = current_describe

    def some_method():
        pass

    fit(some_method)
    expect(current_describe.it_blocks).to_have_length(1)
    expect(current_describe.it_blocks[0].method).to_be(some_method)


def test__fit__flags_the_it_block_as_focused():
    current_describe = DescribeBlock(None, None, None)
    test_collection.current_describe = current_describe

    def some_method():
        pass

    fit(some_method)
    expect(current_describe.it_blocks[0].focused).to_be(True)


def test__fit__flags_ancestors_as_having_focused_descendant():
    grandparent_describe = DescribeBlock(None, None, None)
    parent_describe = DescribeBlock(grandparent_describe, None, None)
    current_describe = DescribeBlock(parent_describe, None, None)
    test_collection.current_describe = current_describe

    def some_method():
        pass

    fit(some_method)
    expect(current_describe.has_focused_descendants).to_be(True)
    expect(parent_describe.has_focused_descendants).to_be(True)
    expect(grandparent_describe.has_focused_descendants).to_be(True)


def test__fdescribe__flags_ancestors_as_having_focused_descendant():
    grandparent_describe = DescribeBlock(None, None, None)
    parent_describe = DescribeBlock(grandparent_describe, None, None)
    current_describe = DescribeBlock(parent_describe, None, None)
    test_collection.current_describe = current_describe

    def some_method():
        pass

    fdescribe("some context")(some_method)

    expect(current_describe.has_focused_descendants).to_be(True)
    expect(parent_describe.has_focused_descendants).to_be(True)
    expect(grandparent_describe.has_focused_descendants).to_be(True)


def test__fdescribe__adds_a_describe_block_to_current_describe():
    current_describe = DescribeBlock(None, None, None)
    test_collection.current_describe = current_describe

    def some_method():
        pass

    fdescribe("some context")(some_method)
    expect(current_describe.describe_blocks).to_have_length(1)
    expect(current_describe.describe_blocks[0].method).to_be(some_method)


def test__fdescribe__flags_the_it_block_as_focused():
    current_describe = DescribeBlock(None, None, None)
    test_collection.current_describe = current_describe

    def some_method():
        pass

    fdescribe("some context")(some_method)
    expect(current_describe.describe_blocks[0].focused).to_be(True)


def test__describe__adds_describe_block_to_current_describe():
    current_describe = DescribeBlock(None, None, None)
    test_collection.current_describe = current_describe

    def some_method():
        pass

    describe(some_method)

    expect(current_describe.describe_blocks).to_have_length(1)
    expect(current_describe.describe_blocks[0].method).to_be(some_method)


def test__describe__when_using_string_description__adds_describe_block_to_current_describe():
    current_describe = DescribeBlock(None, None, None)
    test_collection.current_describe = current_describe

    def some_method():
        pass

    describe("some context")(some_method)

    expect(current_describe.describe_blocks).to_have_length(1)
    expect(current_describe.describe_blocks[0].method).to_be(some_method)


def test__describe__when_using_string_description__sets_description():
    current_describe = DescribeBlock(None, None, None)
    test_collection.current_describe = current_describe

    def some_method():
        pass

    describe("some awesome description")(some_method)

    expect(current_describe.describe_blocks[0].description).to_be("some awesome description")


def test__before_each__adds_before_each_block_to_current_describe():
    current_describe = DescribeBlock(None, None, None)
    test_collection.current_describe = current_describe

    def some_method():
        pass

    before_each(some_method)
    expect(current_describe.before_each_blocks).to_have_length(1)
    expect(current_describe.before_each_blocks[0].method).to_be(some_method)

def test__before_first__adds_before_first_block_to_current_describe():
    current_describe = DescribeBlock(None, None, None)
    test_collection.current_describe = current_describe
    count = []

    @before_first
    def some_method():
        count.append(True)

    current_describe.before_first_blocks[0].method()
    current_describe.before_first_blocks[0].method()
    expect(current_describe.before_first_blocks).to_have_length(1)
    expect(current_describe.before_first_blocks[0].before_first_method).to_be(some_method)
    expect(len(count)).to_be(1)

def test__after_each__adds_after_each_block_to_current_describe():
    current_describe = DescribeBlock(None, None, None)
    test_collection.current_describe = current_describe

    def some_method():
        pass

    after_each(some_method)
    expect(current_describe.after_each_blocks).to_have_length(1)
    expect(current_describe.after_each_blocks[0].method).to_be(some_method)
    expect(current_describe.after_each_blocks[0].description).to_be("@after_each")


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
