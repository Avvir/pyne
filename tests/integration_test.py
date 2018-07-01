from pyne.expectations import expect
from pyne.matchers import contains
from pyne.pyne_result_reporter import reporter
from pyne.pyne_test_collector import it, describe
from pyne.pyne_tester import pyne


def test_reports_failures():
    error = None
    try:
        @pyne
        def some_test_suite():
            @describe
            def some_scenario():
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
    printed_text = []

    def fake_print(text, end=None):
        printed_text.append(text)

    reporter._print = fake_print
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
