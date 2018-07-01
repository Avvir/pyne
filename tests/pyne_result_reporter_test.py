from pyne.expectations import expect
from pyne.pyne_result_reporter import PyneResultReporter

printed_text = []


def fake_print(text, end=None):
    printed_text.append(text)


def test_report_result__when_a_test_fails__it_prints_an_x__the_name_of_the_test__and_the_exception():
    printed_text.clear()
    reporter = PyneResultReporter(fake_print)

    def failing_method():
        expect(1).to_be(2)

    reporter.report_result(failing_method, "some_test_name")

    expect(printed_text[0]).to_be("x")
    expect(printed_text[1]).to_contain("some_test_name")
    expect(printed_text[2]).to_be_a(Exception)


def test_report_result__when_a_test_succeeds__it_prints_a_dot():
    printed_text.clear()
    reporter = PyneResultReporter(fake_print)

    def passing_method():
        pass

    reporter.report_result(passing_method, "some_test_name")

    expect(printed_text[0]).to_be(".")


def test__end_result__when_a_test_has_failed__it_raises_test_failed():
    reporter = PyneResultReporter(fake_print)

    def failing_method():
        expect(True).to_be(False)

    reporter.report_result(failing_method, "some_test_name")
    expect(reporter.report_end_result).to_raise_error_message("Tests failed.")


def test__end_result__when_all_tests_passed__it_prints_success():
    printed_text.clear()
    reporter = PyneResultReporter(fake_print)

    def passing_method():
        pass

    reporter.report_result(passing_method, "some_test_name")

    reporter.report_end_result()

    expect(printed_text[1]).to_be("Success!")


def test__end_result__when_no_tests_run():
    reporter = PyneResultReporter(fake_print)

    expect(reporter.report_end_result).to_raise_error_message("No tests to run!")
