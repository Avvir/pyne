from pynetest.expectations import expect
from pynetest.lib.result_reporters.pyne_result_reporters import ExceptionReporter
from pynetest.lib.pyne_test_blocks import ItBlock


def test__report_end_result__when_a_test_has_failed__it_raises_test_failed():
    reporter = ExceptionReporter()

    it_block = ItBlock(None, None, None)
    reporter.report_failure(it_block, it_block, Exception("some exception"), 0)

    expect(reporter.report_end_result).to_raise_error_with_message("Tests failed.")


def test__report_end_result__when_no_tests_run__raises_error():
    reporter = ExceptionReporter()

    expect(reporter.report_end_result).to_raise_error_with_message("No tests to run!")
