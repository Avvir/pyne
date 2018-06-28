from tests.test_helpers.test_framework.expectations import expect
from tests.test_helpers.test_framework.test_collector import it, reset, describe, before_each
from tests.test_helpers.test_framework.tester import pyne


def test__pyne__collects_tests():
    things_run = []

    def ran_thing(tag):
        things_run.append(tag)

    def some_tests():
        @describe
        def when_there_are_tests():
            @before_each
            def do(self):
                ran_thing("before1")

            @it
            def does_something(self):
                ran_thing("it1")

    pyne(some_tests)

    expect(things_run).to_be(["before1", "it1"])


def test_pyne_decoration_runs_tests():
    things_run = []

    def ran_thing(tag):
        things_run.append(tag)

    @pyne
    def first_test():
        @before_each
        def do(self):
            ran_thing("before1")

        @it
        def does_something(self):
            ran_thing("it1")

    expect(things_run).to_be(["before1", "it1"])


