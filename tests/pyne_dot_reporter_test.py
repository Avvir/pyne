from pyne.expectations import expect
from pyne.pyne_result_reporters import PyneDotReporter
from pyne.pyne_test_blocks import ItBlock

printed_text = []


def fake_print(text, end=None):
    printed_text.append(text)


def test__report_failure__prints_an_x():
    reporter = PyneDotReporter(fake_print)
    it_block = ItBlock(None, None, None)
    printed_text.clear()

    reporter.report_failure(it_block, it_block, Exception("some exception"), 1000)

    expect(printed_text[0]).to_be("x")


def test__report_success__prints_a_dot():
    reporter = PyneDotReporter(fake_print)

    it_block = ItBlock(None, None, None)
    printed_text.clear()

    reporter.report_success(it_block, 0)

    expect(printed_text[0]).to_be(".")
