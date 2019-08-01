"""Pyne tests for pynetest.expectations"""
from pynetest.expectations import expect
from pynetest.pyne_test_collector import it, describe
from pynetest.pyne_tester import pyne

# flake8: noqa
# pylint: disable=missing-docstring, unused-argument
from pynetest.test_doubles.stub import spy_on
from tests.test_helpers.some_class import SomeClass


def expect_assertion_error(fun):
    try:
        fun()
        failed = True
    except AssertionError:
        failed = False
    if failed:
        raise AssertionError(
            "Expected AssertionError to be raised, and none was.")


@pyne
def expectations_tests():
    @describe("#to_raise_error_with_message")
    def _():
        @it("passes when such a message is raised.")
        def _(self):
            def good_fun():
                raise Exception("Matching message!")
            expect(good_fun).to_raise_error_with_message("Matching message!")

        @it("fails when a different message is raised.")
        def _(self):
            def bad_fun():
                raise Exception("Non-matching message!")

            def test_fun():
                expect(bad_fun).to_raise_error_with_message(
                    "Matching message!")
            expect_assertion_error(test_fun)

        @it("fails when no error is raised.")
        def _(self):
            def bad_fun():
                pass

            def test_fun():
                expect(bad_fun).to_raise_error_with_message(
                    "Matching message!")
            expect_assertion_error(test_fun)

    @describe("#to_raise_error_of_type")
    def _():
        @it("can pass")
        def _(self):
            def good_fun():
                raise StopIteration("Bad stuff happened.")
            expect(good_fun).to_raise_error_of_type(StopIteration)

        @describe("when a different type of error is raised")
        def _():
            @it("fails")
            def _(self):
                def bad_fun():
                    raise StopIteration("Bad stuff happended.")

                def test_fun():
                    expect(bad_fun).to_raise_error_of_type(IOError)
                expect_assertion_error(test_fun)

        @it("fails when no error is raised.")
        def _(self):
            def bad_fun():
                pass

            def test_fun():
                expect(bad_fun).to_raise_error_of_type(StopIteration)
            expect_assertion_error(test_fun)

    @describe("#to_be_none")
    def _():
        @it("passes if the value is None")
        def _(self):
            expect(None).to_be_none()

        @it("fails if the value is not None")
        def _(self):
            expect_assertion_error(lambda: expect(5).to_be_none())

    @describe("#not_to_be_none")
    def _():
        @it("passes when the value is not None")
        def _(self):
            expect(5).not_to_be_none()

        @it("fails when the value is None")
        def _(self):
            expect_assertion_error(lambda: expect(None).not_to_be_none())

    @describe("#to_contain")
    def _():
        @it("can pass for an element in a set")
        def _(self):
            expect({5, 10, 3}).to_contain(5)

        @it("fails if the element is not in the set")
        def _(self):
            expect_assertion_error(lambda: expect({5, 10, 3}).to_contain(1000))

    @describe("#not_to_contain")
    def _():
        @it("it passes if the element is not in the set")
        def _(self):
            expect({5, 10, 3}).not_to_contain(100)

        @it("it fails if the element is in the set")
        def _(self):
            expect_assertion_error(lambda: expect({5, 10, 3}).not_to_contain(5))

    @describe("#was_called")
    def _():
        @it("it passes if the method is called")
        def _(self):
            some_instance = SomeClass()
            with spy_on(some_instance.some_method):
                some_instance.some_method()
                expect(some_instance.some_method).was_called()

        @it("it fails if the method is not called")
        def _(self):
            some_instance = SomeClass()
            with spy_on(some_instance.some_method):
                expect_assertion_error(lambda: expect(some_instance.some_method).was_called())

        @it("it fails if the method is not tracked")
        def _(self):
            some_instance = SomeClass()
            expect_assertion_error(lambda: expect(some_instance.some_method).was_called())

    @describe("#was_not_called")
    def _():
        @it("it passes if the method is not called")
        def _(self):
            some_instance = SomeClass()
            with spy_on(some_instance.some_method):
                expect(some_instance.some_method).was_not_called()

        @it("it fails if the method is called")
        def _(self):
            some_instance = SomeClass()
            with spy_on(some_instance.some_method):
                some_instance.some_method()
                expect_assertion_error(lambda: expect(some_instance.some_method).was_not_called())

        @it("it fails if the method is not tracked")
        def _(self):
            some_instance = SomeClass()
            expect_assertion_error(lambda: expect(some_instance.some_method).was_not_called())
