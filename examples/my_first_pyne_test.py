from pyne.expectations import expect
from pyne.pyne_test_collector import it, describe
from pyne.pyne_tester import pyne


@pyne
def my_first_test():
    @describe
    def when_there_are_lots_of_tests():
        @it
        def prints_a_dot_for_each_one(self):
            pass

        @it
        def prints_a_dot_for_each_one(self):
            pass

        @it
        def prints_a_dot_for_each_one(self):
            pass

        @it
        def prints_a_dot_for_each_one(self):
            pass

    @it
    def can_have_expectations(self):
        expect(1).to_be(1)


@pyne
def a_failing_group():
    @describe
    def when_there_are_lots_of_tests():
        @it
        def prints_a_dot_for_each_one(self):
            pass

        @it
        def prints_a_dot_for_each_one(self):
            pass

        @it
        def prints_a_dot_for_each_one(self):
            pass

        @it
        def failing_tests_print_x(self):
            raise Exception("some error")

        @it
        def prints_a_dot_for_each_one(self):
            pass

        @it
        def prints_a_dot_for_each_one(self):
            pass

        @it
        def prints_a_dot_for_each_one(self):
            pass

        @it
        def prints_a_dot_for_each_one(self):
            pass
