"""Pyne tests for pyne.expectations"""
from pyne.expectations import expect
from pyne.pyne_test_collector import it, describe, fdescribe
from pyne.pyne_tester import pyne

# flake8: noqa
# pylint: disable=missing-docstring, unused-argument

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
    @describe("When we expect an error to be raised a message")
    def _():
        @it("it passes when such a message is raised.")
        def _(self):
            def good_fun():
                raise Exception("Matching message!")
            expect(good_fun).to_raise_error_with_message("Matching message!")

        @it("it fails when a different message is raised.")
        def _(self):
            def bad_fun():
                raise Exception("Non-matching message!")

            def test_fun():
                expect(bad_fun).to_raise_error_with_message(
                    "Matching message!")
            expect_assertion_error(test_fun)

        @it("it fails when no error is raised.")
        def _(self):
            def bad_fun():
                pass

            def test_fun():
                expect(bad_fun).to_raise_error_with_message(
                    "Matching message!")
            expect_assertion_error(test_fun)

    @describe("When we expect an error of a type to be raised")
    def _():
        @it("it passes when such a message is raised.")
        def _(self):
            def good_fun():
                raise StopIteration("Bad stuff happened.")
            expect(good_fun).to_raise_error_of_type(StopIteration)

        @it("it fails when a different type is raised.")
        def _(self):
            def bad_fun():
                raise StopIteration("Bad stuff happended.")

            def test_fun():
                expect(bad_fun).to_raise_error_of_type(IOError)
            expect_assertion_error(test_fun)

        @it("it fails when no error is raised.")
        def _(self):
            def bad_fun():
                pass

            def test_fun():
                expect(bad_fun).to_raise_error_of_type(StopIteration)
            expect_assertion_error(test_fun)

    @describe("When we check for None")
    def _():
        @it("it passes if the value is None")
        def _(self):
            expect(None).to_be_none()

        @it("it fails if the value is not None")
        def _(self):
            expect_assertion_error(lambda: expect(5).to_be_none())

    @describe("When we check for not None")
    def _():
        @it("it passes if the value is not None")
        def _(self):
            expect(5).not_to_be_none()

        @it("it fails if the value is None")
        def _(self):
            expect_assertion_error(lambda: expect(None).not_to_be_none())

    @describe("When we check for a collection to contain an element")
    def _():
        @it("it passes if the element is in the set")
        def _(self):
            test_set = set([5, 10, 3])
            expect(test_set).to_contain(5)

        @it("it fails if the element is not in the set")
        def _(self):
            test_set = set([5, 10, 3])
            expect_assertion_error(lambda: expect(test_set).to_contain(1000))

    @describe("When we check for a collection to not contain an element")
    def _():
        @it("it passes if the element is not in the set")
        def _(self):
            test_set = set([5, 10, 3])
            expect(test_set).not_to_contain(100)

        @it("it fails if the element is in the set")
        def _(self):
            test_set = set([5, 10, 3])
            expect_assertion_error(lambda: expect(test_set).not_to_contain(5))
