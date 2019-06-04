from pynetest.expectations import expect
from pynetest.lib.result_reporters.printing_reporter import PrintingReporter
from pynetest.lib.result_reporters.pyne_result_reporters import PyneTreeReporter
from pynetest.lib.pyne_test_blocks import DescribeBlock, ItBlock
from tests.test_helpers.fake_print import printed_text, StubPrint


def test__report_enter_context__prints_context_description():
    with StubPrint():
        describe_block = DescribeBlock(None, "Some context description", None)
        reporter = PrintingReporter(PyneTreeReporter())
        printed_text.clear()

        reporter.report_enter_context(describe_block)

        expect(printed_text[0]).to_contain("Some context description")


def test__report_enter_context__indents_based_on_tree_depth():
    with StubPrint():
        describe_block = DescribeBlock(None, "Some context description", None)
        reporter = PrintingReporter(PyneTreeReporter())
        printed_text.clear()

        reporter.report_enter_context(describe_block)
        reporter.report_enter_context(describe_block)
        reporter.report_enter_context(describe_block)

        first_indent = printed_text[0].find("Some context")
        expect(printed_text[1].find("Some context")).to_be(first_indent + 2)
        expect(printed_text[2].find("Some context")).to_be(first_indent + 4)


def test__report_success__prints_test_description():
    with StubPrint():
        it_block = ItBlock(None, "Some it block description", None)
        reporter = PrintingReporter(PyneTreeReporter())
        printed_text.clear()

        reporter.report_success(it_block, 0)

        expect(printed_text[0]).to_contain("Some it block description")


def test__report_success__indents_based_on_tree_depth():
    with StubPrint():
        describe_block = DescribeBlock(None, "Some context description", None)
        it_block = ItBlock(None, "Some it block description", None)
        reporter = PrintingReporter(PyneTreeReporter())
        printed_text.clear()

        reporter.report_enter_context(describe_block)
        reporter.report_success(it_block, 0)

        reporter.report_enter_context(describe_block)
        reporter.report_success(it_block, 0)

        reporter.report_enter_context(describe_block)
        reporter.report_success(it_block, 0)

        first_index = printed_text[1].find("Some it")
        expect(printed_text[3].find("Some it")).to_be(first_index + 2)
        expect(printed_text[5].find("Some it")).to_be(first_index + 4)


def test__report_failure__prints_test_description():
    with StubPrint():
        it_block = ItBlock(None, "Some it block description", None)
        reporter = PrintingReporter(PyneTreeReporter())
        printed_text.clear()

        reporter.report_failure(it_block, it_block, Exception("some exception"), 0)

        expect(printed_text[0]).to_contain("Some it block description")


def test__report_failure__indents_based_on_tree_depth():
    with StubPrint():
        describe_block = DescribeBlock(None, "Some context description", None)
        it_block = ItBlock(None, "Some it block description", None)
        reporter = PrintingReporter(PyneTreeReporter())
        printed_text.clear()

        reporter.report_enter_context(describe_block)
        reporter.report_failure(it_block, it_block, Exception(), 0)

        reporter.report_enter_context(describe_block)
        reporter.report_failure(it_block, it_block, Exception(), 0)

        reporter.report_enter_context(describe_block)
        reporter.report_failure(it_block, it_block, Exception(), 0)

        first_index = printed_text[1].find("Some it")
        expect(printed_text[3].find("Some it")).to_be(first_index + 2)
        expect(printed_text[5].find("Some it")).to_be(first_index + 4)


def test__report_pending__prints_test_description():
    with StubPrint():
        it_block = ItBlock(None, "Some it block description", None)
        reporter = PrintingReporter(PyneTreeReporter())

        reporter.report_pending(it_block)

        expect(printed_text[0]).to_contain("Some it block description")


def test__report_pending__indents_based_on_tree_depth():
    with StubPrint():
        describe_block = DescribeBlock(None, "Some context description", None)
        it_block = ItBlock(None, "Some it block description", None)
        reporter = PrintingReporter(PyneTreeReporter())

        reporter.report_enter_context(describe_block)
        reporter.report_pending(it_block)

        reporter.report_enter_context(describe_block)
        reporter.report_pending(it_block)

        reporter.report_enter_context(describe_block)
        reporter.report_pending(it_block)

        first_index = printed_text[1].find("Some it")
        expect(printed_text[3].find("Some it")).to_be(first_index + 2)
        expect(printed_text[5].find("Some it")).to_be(first_index + 4)
