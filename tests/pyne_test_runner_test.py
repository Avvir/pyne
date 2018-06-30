from pyne.expectations import expect
from pyne.matchers import anything
from pyne.pyne_test_collector import reset, it, describe, test_collection, before_each
from pyne.pyne_test_runner import run_tests


def test__when_there_is_an_it__runs_the_it():
    reset()
    context = test_collection.current_describe.context
    context.call_count = 0

    @it
    def do_something(self):
        self.call_count += 1

    run_tests(test_collection.top_level_describe)
    expect(context.call_count).to_be(1)


def test__when_a_test_fails__raises_an_error():
    reset()

    @it
    def failing_test(self):
        expect(1).to_be(2)

    expect(lambda: run_tests(test_collection.current_describe)) \
        .to_raise_error_message(anything())


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

    run_tests(test_collection.top_level_describe)

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
    run_tests(nested_describe)

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
    run_tests(test_collection.top_level_describe)

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
    run_tests(test_collection.top_level_describe)

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
        run_tests(test_collection.top_level_describe)
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
        run_tests(test_collection.top_level_describe)
    except Exception:
        pass
    finally:
        expect(context.calls).to_be(["some-it"])
