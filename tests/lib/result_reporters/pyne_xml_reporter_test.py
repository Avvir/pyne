import os
import random

from pynetest.expectations import expect
from pynetest.lib.result_reporters.printing_reporter import PrintingReporter
from pynetest.lib.result_reporters.pyne_result_reporters import PyneXmlReporter
from pynetest.lib.pyne_test_blocks import ItBlock
from tests.test_helpers.fake_print import StubPrint, printed_text


def some_tmp_path(path):
    random_string = "%030x" % random.randrange(16**30)
    directory = "/tmp/avvir_pynetest/" + random_string
    os.makedirs(directory)
    return directory + "/" + path


def test__report_end_result__when_env_var_not_set__output_nothing():
    if "PYNETEST_XML_REPORT" in os.environ:
        del os.environ["PYNETEST_XML_REPORT"]

    with StubPrint():
        reporter = PrintingReporter(PyneXmlReporter())

        printed_text.clear()

        reporter.report_end_result()

        expect(printed_text[0]).to_be("")


def test__report_end_result__when_a_test_has_failed__it_stores_stats():
    os.environ["PYNETEST_XML_REPORT"] = some_tmp_path("output.xml")

    with StubPrint():
        reporter = PrintingReporter(PyneXmlReporter())

        it_block = ItBlock(None, None, None)
        reporter.report_failure(it_block, it_block, Exception("some exception\x1b"), 1000)
        reporter.report_success(it_block, 500)
        reporter.report_success(it_block, 500)

        printed_text.clear()

        reporter.report_end_result()

        expect(printed_text[0]).to_contain("Exported results to")
        expect(printed_text[0]).to_contain("output.xml")
        expect(os.path.exists(os.environ["PYNETEST_XML_REPORT"])).to_be(True)
        with open(os.environ["PYNETEST_XML_REPORT"]) as file:
            expect(file.read()).not_to_contain("\x1b")


def test__report_end_result__when_all_tests_passed__it_stores_stats():
    os.environ["PYNETEST_XML_REPORT"] = some_tmp_path("output.xml")

    with StubPrint():
        reporter = PrintingReporter(PyneXmlReporter())

        it_block = ItBlock(None, None, None)
        reporter.report_success(it_block, 1000)
        reporter.report_success(it_block, 500)
        printed_text.clear()

        reporter.report_end_result()

        expect(printed_text[0]).to_contain("Exported results to")
        expect(printed_text[0]).to_contain("output.xml")
        expect(os.path.exists(os.environ["PYNETEST_XML_REPORT"])).to_be(True)


def test__report_end_result__when_no_tests_run__it_stores_stats():
    os.environ["PYNETEST_XML_REPORT"] = some_tmp_path("my-file.xml")

    with StubPrint():
        reporter = PrintingReporter(PyneXmlReporter())

        printed_text.clear()

        reporter.report_end_result()

        expect(printed_text[0]).to_contain("Exported results to")
        expect(printed_text[0]).to_contain("my-file.xml")
        expect(os.path.exists(os.environ["PYNETEST_XML_REPORT"])).to_be(True)
