import re

from pyne.expectations import expect
from pyne.pyne_test_collector import it, describe, before_each, xit, xdescribe
from pyne.pyne_tester import pyne


@pyne
def my_first_test():
    @describe
    def when_there_are_lots_of_tests():
        @it
        def prints_a_result_for_each_one(self):
            pass

        @it
        def prints_a_result_for_each_one(self):
            pass

        @it
        def prints_a_result_for_each_one(self):
            pass

        @describe("When things are nested further")
        def _():
            @it
            def prints_inner_results(self):
                pass

            @xit("can be pending")
            def _(self):
                pass

        @describe("When things are nested further")
        def _():
            @it
            def prints_inner_results(self):
                pass

        @xdescribe("a whole group can be pending")
        def _():
            @it
            def prints_inner_results(self):
                pass

            @describe("When things are nested further")
            def _():
                @it
                def prints_inner_results(self):
                    pass

        @it
        def prints_a_result_for_each_one(self):
            pass

    @it
    def can_have_expectations(self):
        expect(1).to_be(1)


# @pyne
def a_failing_group():
    @describe
    def when_there_are_lots_of_tests():
        @it
        def prints_a_result_for_each_one(self):
            pass

        @it
        def prints_a_result_for_each_one(self):
            pass

        @it
        def prints_a_result_for_each_one(self):
            pass

        @it
        def failing_tests_print_x(self):
            raise Exception("some error")

        @it
        def prints_a_result_for_each_one(self):
            pass

        @it
        def prints_a_result_for_each_one(self):
            pass

        @it
        def prints_a_result_for_each_one(self):
            pass

        @describe("When things are nested further")
        def _():
            @before_each
            def do(self):
                raise Exception("some setup error")

            @it
            def prints_inner_results(self):
                pass
        @it
        def prints_a_result_for_each_one(self):
            pass


class Calculator:

    def calculate(self, expression):
        if re.search("[ \d\s+-]+", expression):
            return eval(expression)
        else:
            raise Exception("invalid expression")


@pyne
def _calculate():
    @before_each
    def do(self):
        self.calculator = Calculator()

    @it("can add two numbers together")
    def _(self):
        expect(self.calculator.calculate("1 + 1")).to_be(2)

    @it("can subtract")
    def _(self):
        expect(self.calculator.calculate("2 - 1")).to_be(1)

    @it("does not run arbitrary code")
    def _(self):
        def extra_method(self):
            self.__format__ = lambda s: "Some Broken Calculator"

        self.calculator.extra_method = extra_method
        expect(
            lambda: self.calculator.calculate('self.extra_method(self)')
        ).to_raise_error_message("invalid expression")

        expect(self.calculator.__format__("")).not_to_be("Some Broken Calculator")
