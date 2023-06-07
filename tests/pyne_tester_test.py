from distributed.client import Client
from pynetest.expectations import expect
from pynetest.pyne_test_collector import it, describe, before_each
from pynetest.pyne_tester import pyne


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
        def _(self):
            ran_thing("before1")

        @it("does something")
        def _(self):
            ran_thing("it1")

    expect(things_run).to_be(["before1", "it1"])

def test__when_a_multiprocessing_loop_is_created__runs_the_tests_only_in_the_main_entrypoint():
    things_run = []

    def ran_thing(tag):
        things_run.append(tag)
    @pyne
    def first_test():
        @it("does something")
        def _(self):
            print(f'_')
            Client()
            ran_thing("it1")
    expect(things_run).to_be(['it1'])

