import re

from pyne.expectations import expect
from pyne.pyne_test_collector import before_each, it
from pyne.pyne_tester import pyne


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