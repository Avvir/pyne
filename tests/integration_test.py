from pynetest.expectations import expect
from pynetest.matchers import contains
from pynetest.pyne_test_collector import it, describe, before_each, after_each, xit, xdescribe, fit, fdescribe
from pynetest.pyne_tester import pyne
from tests.test_helpers.fake_print import printed_text, StubPrint


def test_reports_failures():
    error = None
    try:
        @pyne
        def some_test_suite():
            @describe("some scenario")
            def _():
                @it
                def some_test(self):
                    pass

            @describe
            def some_other_scenario():
                @it
                def some_failing_test(self):
                    raise Exception("some failing test")

            @it
            def some_passing_test(self):
                pass
    except Exception as e:
        error = e
    finally:
        expect(error.args[0]).to_contain("failed")


def test_reports_the_name_of_failed_tests():
    with StubPrint() as print:
        try:
            @pyne
            def some_test_suite():
                @describe
                def some_scenario():
                    @it
                    def some_failing_test(self):
                        raise Exception("some exception")

                @it
                def some_passing_test(self):
                    pass
        except Exception:
            pass
        finally:
            expect(printed_text).to_contain(contains("some_failing_test"))


def test__when_a_before_each_fails__reports_the_name_of_failed_tests():
    with StubPrint():
        try:
            @pyne
            def some_test_suite():
                @before_each
                def some_failing_setup(self):
                    raise Exception("some exception")

                @it("some test")
                def _(self):
                    pass

                @it
                def some_other_test(self):
                    pass

        except Exception:
            pass
        finally:
            expect(printed_text).to_contain(contains("@before_each"))
            expect(printed_text).to_contain(contains("some test"))
            expect(printed_text).to_contain(contains("some_other_test"))


def test__when_a_test_is_pending__reports_there_are_pending_tests():
    with StubPrint():
        @pyne
        def some_test_suite():
            @it("some test")
            def _(self):
                pass

            @xit
            def some_other_test(self):
                pass

        expect(printed_text).to_contain(contains("pending"))


def test__when_a_describe_block_is_pending__reports_there_are_pending_tests():
    with StubPrint():
        @pyne
        def some_test_suite():
            @it("some test")
            def _(self):
                pass

            @xdescribe("some tests")
            def _():
                @it
                def some_other_test(self):
                    pass

        expect(printed_text).to_contain(contains("pending"))


def test__when_a_before_each_fails__does_not_run_tests_that_depend_on_the_before_block():
    calls = []
    try:
        @pyne
        def some_test_suite():
            @before_each
            def some_failing_setup(self):
                self.calls = calls
                raise Exception("some exception")

            @it
            def some_test(self):
                self.calls.append("it1")

            @it
            def some_other_test(self):
                self.calls.append("it2")

    except Exception:
        pass
    finally:
        expect(calls).to_have_length(0)


def test__when_a_before_each_fails__still_runs_the_after_each():
    calls = []
    try:
        @pyne
        def some_test_suite():
            @before_each
            def some_failing_setup(self):
                self.calls = calls
                raise Exception("some exception")

            @it("does something")
            def some_test(self):
                self.calls.append("it1")

            @after_each
            def some_after_each(self):
                self.calls.append("some_after_each")

    except Exception:
        pass
    finally:
        expect(calls).to_be(["some_after_each"])


def test__when_a_test_is_focused__skips_other_tests():
    calls = []

    @pyne
    def some_test_suite():
        @before_each
        def _(self):
            self.calls = calls

        @it
        def some_other_test(self):
            self.calls.append("it1")

        @fit
        def some_test(self):
            self.calls.append("it2")

        @it
        def some_other_test(self):
            self.calls.append("it3")

    expect(calls).to_have_length(1)


def test__when_a_describe_is_focused__skips_other_tests():
    calls = []

    @pyne
    def some_test_suite():
        @before_each
        def _(self):
            self.calls = calls

        @it
        def some_other_test(self):
            self.calls.append("it1")

        @fdescribe("some test")
        def _():
            @it("does something")
            def _(self):
                self.calls.append("it2")

        @it
        def some_other_test(self):
            self.calls.append("it3")

    expect(calls).to_be(["it2"])
