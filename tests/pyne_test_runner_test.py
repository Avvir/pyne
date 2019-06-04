from time import sleep

from pynetest.expectations import expect
from pynetest.matchers import anything, at_least
from pynetest.lib.result_reporters.pyne_result_reporters import ExceptionReporter, StatTrackingReporter
from pynetest.lib.pyne_test_blocks import ItBlock, DescribeBlock
from pynetest.pyne_test_collector import reset, it, describe, test_collection, before_each, after_each
from pynetest.pyne_test_runner import run_tests


def test__when_there_is_an_it__runs_the_it():
    reset()
    context = test_collection.current_describe.context
    context.call_count = 0

    @it
    def do_something(self):
        self.call_count += 1

    run_tests(test_collection.top_level_describe, ExceptionReporter())
    expect(context.call_count).to_be(1)


def test__when_there_is_an_it__reports_the_timing():
    reset()
    context = test_collection.current_describe.context

    @before_each
    def _(self):
        sleep(0.05)

    @it("does something")
    def _(self):
        sleep(0.04)

    reporter = ExceptionReporter()
    run_tests(test_collection.top_level_describe, reporter)
    expect(reporter.stats.total_timing_millis).to_be(at_least(90))


def test__when_a_test_fails__raises_an_error():
    reset()

    @it
    def failing_test(self):
        expect(1).to_be(2)

    expect(lambda: run_tests(test_collection.current_describe, ExceptionReporter())) \
        .to_raise_error_with_message(anything())


def test__when_there_is_a_before_each__runs_it_before_each_test():
    reset()
    context = test_collection.current_describe.context
    context.calls = []

    @before_each
    def do(self):
        self.calls.append("before")

    @it
    def first(self):
        self.calls.append("it1")

    @it
    def second(self):
        self.calls.append("it2")

    run_tests(test_collection.top_level_describe, ExceptionReporter())

    expect(context.calls).to_be(["before", "it1", "before", "it2"])


def test__when_there_are_before_each_blocks_in_parent_describes__runs_them_before_each_test():
    reset()
    context = test_collection.current_describe.context
    context.calls = []

    @describe
    def when_context_1():
        @before_each
        def do(self):
            self.calls.append("before1")

        @describe
        def when_context_2():
            @before_each
            def do(self):
                self.calls.append("before2")

            @describe
            def when_context_3():
                @before_each
                def do(self):
                    self.calls.append("before3")

                @it
                def do_first_thing(self):
                    self.calls.append("it1")

                @it
                def do_second_thing(self):
                    self.calls.append("it2")

    outer_describe = test_collection.current_describe.describe_blocks[0]
    test_collection.collect_describe(outer_describe)

    blocks_ = outer_describe.describe_blocks[0]
    nested_describe = blocks_.describe_blocks[0]
    run_tests(nested_describe, ExceptionReporter())

    expect(context.calls).to_be(["before1", "before2", "before3", "it1", "before1", "before2", "before3", "it2"])


def test__when_there_are_nested_describes__it_runs_them():
    reset()
    context = test_collection.current_describe.context
    context.calls = []

    @describe
    def when_context_1():
        @it
        def do_first_thing(self):
            self.calls.append("it1")

        @describe
        def when_context_2():
            @describe
            def when_context_3():
                @it
                def do_second_thing(self):
                    self.calls.append("it2")

            @describe
            def when_context_4():
                @it
                def do_third_thing(self):
                    self.calls.append("it3")

                @it
                def do_fourth_thing(self):
                    self.calls.append("it4")

    outer_describe = test_collection.current_describe.describe_blocks[0]
    test_collection.collect_describe(outer_describe)
    run_tests(test_collection.top_level_describe, ExceptionReporter())

    expect(context.calls).to_be(["it1", "it2", "it3", "it4"])


def test__when_there_are_before_each_blocks_for_another_describe__it_doesnt_run_them():
    reset()
    context = test_collection.current_describe.context
    context.calls = []

    @describe
    def when_context_1():
        @describe
        def when_context_2():
            @before_each
            def do(self):
                self.calls.append("before1")

        @describe
        def when_context_3():
            @it
            def do_something_1(self):
                self.calls.append("it1")

    outer_describe = test_collection.current_describe.describe_blocks[0]
    test_collection.collect_describe(outer_describe)
    run_tests(test_collection.top_level_describe, ExceptionReporter())

    expect(context.calls).to_be(["it1"])


def test__when_a_test_fails__it_continues_running_tests():
    reset()
    context = test_collection.current_describe.context
    context.calls = []

    @it
    def do_first_thing(self):
        self.calls.append("it1")
        raise Exception("Some First Exception")

    @it
    def do_second_thing(self):
        self.calls.append("it2")

    try:
        run_tests(test_collection.top_level_describe, ExceptionReporter())
    except Exception:
        pass
    finally:
        expect(context.calls).to_be(["it1", "it2"])


def test__when_a_before_block_fails__it_runs_it_blocks_in_the_next_describe():
    reset()
    context = test_collection.current_describe.context
    context.calls = []

    @describe
    def outer_describe():
        @describe
        def some_describe():
            @before_each
            def some_before_each_that_raises(self):
                raise Exception("Some Setup exception")

            @it
            def some_test():
                pass

        @describe
        def some_second_describe():
            @it
            def some_second_test(self):
                self.calls.append("some-it")

    outer_describe = test_collection.current_describe.describe_blocks[0]
    test_collection.collect_describe(outer_describe)
    try:
        run_tests(test_collection.top_level_describe, ExceptionReporter())
    except Exception:
        pass
    finally:
        expect(context.calls).to_be(["some-it"])


def test__when_a_test_is_pended__it_does_not_run_the_test():
    reset()
    context = test_collection.current_describe.context
    context.calls = []

    def it1(self):
        self.calls.append("it1")

    test_collection.current_describe.it_blocks = [
        ItBlock(test_collection.current_describe, "some test", it1, pending=True)
    ]

    run_tests(test_collection.current_describe, StatTrackingReporter())

    expect(context.calls).to_have_length(0)


def test__when_a_test_is_pended__it_reports_the_test_as_pending():
    reset()
    context = test_collection.current_describe.context
    context.calls = []

    def it1(self):
        self.calls.append("it1")

    test_collection.current_describe.it_blocks = [
        ItBlock(test_collection.current_describe, "some test", it1, pending=True)
    ]

    reporter = StatTrackingReporter()
    run_tests(test_collection.current_describe, reporter)

    expect(reporter.stats.test_count).to_be(1)
    expect(reporter.stats.pending_count).to_be(1)


def test__when_a_describe_block_is_pended__it_reports_the_contained_tests_as_pending():
    reset()

    describe_block = DescribeBlock(None, "some describe", None, pending=True)

    def it1(self):
        pass

    describe_block.it_blocks = [
        ItBlock(describe_block, "some test", it1)
    ]

    reporter = StatTrackingReporter()
    run_tests(describe_block, reporter)

    expect(reporter.stats.test_count).to_be(1)
    expect(reporter.stats.pending_count).to_be(1)


def test__when_a_describe_block_with_nested_describes_is_pended__it_reports_the_contained_tests_as_pending():
    reset()

    describe_block = DescribeBlock(None, "some describe", None, pending=True)
    inner_describe = DescribeBlock(describe_block, "some inner description", None)
    describe_block.describe_blocks = [inner_describe]

    def it1(self):
        pass

    inner_describe.it_blocks = [
        ItBlock(describe_block, "some test", it1)
    ]

    reporter = StatTrackingReporter()
    run_tests(describe_block, reporter)

    expect(reporter.stats.test_count).to_be(1)
    expect(reporter.stats.pending_count).to_be(1)


def test__when_a_describe_block_has_focused_descendants__it_runs_only_the_focused_tests():
    reset()

    describe_block = DescribeBlock(None, "some describe", None)
    inner_describe = DescribeBlock(describe_block, "some inner description", None)
    other_inner_describe = DescribeBlock(describe_block, "some other inner description", None)
    describe_block.describe_blocks = [inner_describe, other_inner_describe]

    def it1(self):
        pass

    inner_describe.it_blocks = [
        ItBlock(describe_block, "some test", it1, focused=True),
        ItBlock(describe_block, "some test", it1)
    ]
    describe_block.has_focused_descendants = True
    inner_describe.has_focused_descendants = True

    other_inner_describe.it_blocks = [
        ItBlock(describe_block, "some other test", it1),
        ItBlock(describe_block, "some third test", it1)
    ]

    reporter = StatTrackingReporter()
    run_tests(describe_block, reporter)

    expect(reporter.stats.test_count).to_be(1)


def test__when_a_describe_block_is_focused__it_runs_descendant_tests():
    reset()

    describe_block = DescribeBlock(None, "some describe", None, has_focused_descendants=True)
    inner_describe = DescribeBlock(describe_block, "some inner description", None, focused=True)
    other_inner_describe = DescribeBlock(describe_block, "some other inner description", None)
    describe_block.describe_blocks = [inner_describe, other_inner_describe]

    def it1(self):
        pass

    inner_describe.it_blocks = [
        ItBlock(describe_block, "some test", it1),
        ItBlock(describe_block, "some test", it1)
    ]
    other_inner_describe.it_blocks = [
        ItBlock(describe_block, "some other test", it1),
        ItBlock(describe_block, "some third test", it1)
    ]

    reporter = StatTrackingReporter()
    run_tests(describe_block, reporter)

    expect(reporter.stats.test_count).to_be(2)


def test__when_there_is_a_after_each__runs_it_after_each_test():
    reset()
    context = test_collection.current_describe.context
    context.calls = []

    @after_each
    def do(self):
        self.calls.append("after")

    @it
    def first(self):
        self.calls.append("it1")

    @it
    def second(self):
        self.calls.append("it2")

    run_tests(test_collection.top_level_describe, ExceptionReporter())

    expect(context.calls).to_be(["it1", "after", "it2", "after"])


def test__when_there_are_after_each_blocks_in_parent_describes__runs_them_after_each_test():
    reset()
    context = test_collection.current_describe.context
    context.calls = []

    @describe
    def when_context_1():
        @after_each
        def do(self):
            self.calls.append("after1")

        @describe
        def when_context_2():
            @after_each
            def do(self):
                self.calls.append("after2")

            @describe
            def when_context_3():
                @after_each
                def do(self):
                    self.calls.append("after3")

                @it
                def do_first_thing(self):
                    self.calls.append("it1")

                @it
                def do_second_thing(self):
                    self.calls.append("it2")

    outer_describe = test_collection.current_describe.describe_blocks[0]
    test_collection.collect_describe(outer_describe)

    blocks_ = outer_describe.describe_blocks[0]
    nested_describe = blocks_.describe_blocks[0]
    run_tests(nested_describe, ExceptionReporter())

    expect(context.calls).to_be(["it1", "after1", "after2", "after3", "it2", "after1", "after2", "after3"])
