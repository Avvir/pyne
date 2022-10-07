from pynetest.expectations import expect
from pynetest.lib.pyne_test_blocks import ItBlock, DescribeBlock
from pynetest.lib.result_reporters.printing_reporter import PrintingReporter
from pynetest.lib.result_reporters.pyne_result_reporters import PyneFailuresListReporter
from pynetest.matchers import contains
from tests.test_helpers.fake_print import StubPrint, printed_text


def test__report_brief_description_for_all_failures():
    reporter = PrintingReporter(PyneFailuresListReporter())
    with StubPrint():
        exception = Exception()
        try:
            raise exception
        except Exception as e:
            top_describe_block = DescribeBlock(None, "When Top describe", None)
            describe_block = DescribeBlock(top_describe_block, "When description", None)
            block = ItBlock(describe_block, "It does", None)
            reporter.report_failure(block, block, e, 0)
        reporter.report_end_result()

    expect(printed_text).to_contain(contains("When Top describe >> When description >> It does"))
