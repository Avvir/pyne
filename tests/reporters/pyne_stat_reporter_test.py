from pyne.expectations import expect
from pyne.pyne_result_reporters import PyneStatReporter
from pyne.pyne_test_blocks import ItBlock, DescribeBlock
from tests.test_helpers.fake_print import StubPrint, printed_text


def test__report_failure__increases_the_failure_count():
    reporter = PyneStatReporter()

    it_block = ItBlock(None, None, None)

    reporter.report_failure(it_block, it_block, Exception("some exception"), 0)
    reporter.report_failure(it_block, it_block, Exception("some exception"), 0)

    expect(reporter.stats.failure_count).to_be(2)


def test__report_failure__increases_the_test_run_count():
    reporter = PyneStatReporter()

    it_block = ItBlock(None, None, None)

    reporter.report_failure(it_block, it_block, Exception("some exception"), 0)
    reporter.report_failure(it_block, it_block, Exception("some exception"), 0)

    expect(reporter.stats.test_count).to_be(2)


def test__report_failure__sets_overall_failure():
    reporter = PyneStatReporter()

    it_block = ItBlock(None, None, None)

    reporter.report_failure(it_block, it_block, Exception("some exception"), 0)

    expect(reporter.stats.is_failure).to_be(True)


def test__report_failure__increases_the_total_timing():
    reporter = PyneStatReporter()
    it_block = ItBlock(None, None, None)

    reporter.report_failure(it_block, it_block, Exception("some exception"), 1000)
    reporter.report_failure(it_block, it_block, Exception("some exception"), 20)

    expect(reporter.stats.total_timing_millis).to_be(1020)


def test__report_success__increases_the_test_run_count():
    reporter = PyneStatReporter()

    it_block = ItBlock(None, None, None)

    reporter.report_success(it_block, 0)
    reporter.report_success(it_block, 0)

    expect(reporter.stats.test_count).to_be(2)


def test__report_success__increases_the_passes_count():
    reporter = PyneStatReporter()

    it_block = ItBlock(None, None, None)

    reporter.report_success(it_block, 0)
    reporter.report_success(it_block, 0)

    expect(reporter.stats.pass_count).to_be(2)


def test__report_success__increases_the_total_timing():
    reporter = PyneStatReporter()

    it_block = ItBlock(None, None, None)

    reporter.report_success(it_block, 10)
    reporter.report_success(it_block, 300)

    expect(reporter.stats.total_timing_millis).to_be(310)


def test__report_pending__increases_the_test_run_count():
    reporter = PyneStatReporter()

    it_block = ItBlock(None, None, None)

    reporter.report_pending(it_block)
    reporter.report_pending(it_block)

    expect(reporter.stats.test_count).to_be(2)


def test__report_enter_context__increases_depth():
    reporter = PyneStatReporter()

    describe_block = DescribeBlock(None, None, None)

    reporter.report_enter_context(describe_block)
    expect(reporter.depth).to_be(1)

    reporter.report_enter_context(describe_block)
    expect(reporter.depth).to_be(2)


def test__report_exit_context__decreases_depth():
    reporter = PyneStatReporter()

    describe_block = DescribeBlock(None, None, None)
    reporter.report_enter_context(describe_block)
    reporter.report_enter_context(describe_block)

    reporter.report_exit_context(describe_block)
    expect(reporter.depth).to_be(1)

    reporter.report_exit_context(describe_block)
    expect(reporter.depth).to_be(0)


def test__report_end_result__when_a_test_has_failed__it_prints_stats():
    with StubPrint():
        reporter = PyneStatReporter()

        it_block = ItBlock(None, None, None)
        reporter.report_failure(it_block, it_block, Exception("some exception"), 1000)
        reporter.report_success(it_block, 500)
        reporter.report_success(it_block, 500)

        printed_text.clear()

        reporter.report_end_result()

        expect(printed_text[0]).to_contain("1 failed, 2 passed in 2.00 seconds")


def test__report_end_result__when_all_tests_passed__it_prints_stats():
    with StubPrint():
        reporter = PyneStatReporter()

        it_block = ItBlock(None, None, None)
        reporter.report_success(it_block, 1000)
        reporter.report_success(it_block, 500)
        printed_text.clear()

        reporter.report_end_result()

        expect(printed_text[0]).to_contain("2 passed in 1.50 seconds")


def test__report_end_result__test_is_pending__reports_stats():
    with StubPrint():
        reporter = PyneStatReporter()

        passing_it_block = ItBlock(None, None, None)
        pending_it_block = ItBlock(None, None, None, pending=True)
        reporter.report_success(passing_it_block, 1000)
        reporter.report_pending(pending_it_block)
        printed_text.clear()

        reporter.report_end_result()

        expect(printed_text[0]).to_contain("1 passed, 1 pending in 1.00 seconds")


def test__report_end_result__when_no_tests_run__reports_stats():
    with StubPrint():
        reporter = PyneStatReporter()

        printed_text.clear()

        reporter.report_end_result()

        expect(printed_text[0]).to_contain("Ran 0 tests")


def test__reset__sets_stats_to_0():
    describe_block = DescribeBlock(None, None, None)
    it_block = ItBlock(None, None, None)
    reporter = PyneStatReporter()
    reporter.report_enter_context(describe_block)
    reporter.report_enter_context(describe_block)
    reporter.report_success(it_block, 1000)
    reporter.report_failure(it_block, it_block, Exception("some exception"), 1000)
    reporter.report_failure(it_block, it_block, Exception("some exception"), 1000)

    reporter.reset()

    expect(reporter.stats.pass_count).to_be(0)
    expect(reporter.stats.is_failure).to_be(False)
    expect(reporter.stats.total_timing_millis).to_be(0)
    expect(reporter.stats.failure_count).to_be(0)
    expect(reporter.stats.test_count).to_be(0)
    expect(reporter.depth).to_be(0)
