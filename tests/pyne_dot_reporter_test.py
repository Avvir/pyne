from pyne.expectations import expect
from pyne.matchers import contains_text, instance_of
from pyne.pyne_result_reporters import PyneDotReporter
from pyne.pyne_test_blocks import ItBlock, BeforeEachBlock
from pyne.pyne_test_collector import test_collection

printed_text = []


def fake_print(text, end=None):
    printed_text.append(text)


def test_report_result__when_a_test_fails__it_prints_an_x__the_name_of_the_test__and_the_exception():
    printed_text.clear()
    context = test_collection.top_level_describe.context

    reporter = PyneDotReporter(fake_print)

    def failing_method(self):
        expect(1).to_be(2)

    it_block = ItBlock(test_collection.top_level_describe, "some_test_name", failing_method)

    reporter.report_result(context, [], it_block)

    expect(printed_text[0]).to_be("x")
    expect(printed_text[1]).to_contain("some_test_name")
    expect(printed_text[2]).to_be_a(Exception)


def test_report_result__when_a_test_succeeds__it_prints_a_dot():
    reporter = PyneDotReporter(fake_print)
    context = test_collection.top_level_describe.context

    def passing_method(self):
        pass

    it_block = ItBlock(test_collection.top_level_describe, "some_test_name", passing_method)
    printed_text.clear()

    reporter.report_result(context, [], it_block)

    expect(printed_text[0]).to_be(".")


def test_report_result__when_a_before_block_fails__it_prints_an_x__the_name_of_the_test__and_the_exception():
    printed_text.clear()
    context = test_collection.top_level_describe.context

    reporter = PyneDotReporter(fake_print)

    def passing_method(self):
        pass

    def failing_method(self):
        raise Exception("some exception")

    it_block = ItBlock(test_collection.top_level_describe, "some_test_name", passing_method)
    failing_before = BeforeEachBlock(test_collection.top_level_describe, failing_method)

    reporter.report_result(context, [failing_before], it_block)

    expect(printed_text[0]).to_be("x")
    expect(printed_text).to_contain(contains_text("some_test_name"))
    expect(printed_text).to_contain(instance_of(Exception))


def test_report_result__when_a_before_block_fails__does_not_run_the_it_block():
    context = test_collection.top_level_describe.context
    reporter = PyneDotReporter(fake_print)

    def passing_method(self):
        self.called_it = True

    def failing_method(self):
        raise Exception("some exception")

    it_block = ItBlock(None, "some_test_name", passing_method)
    failing_before = BeforeEachBlock(None, failing_method)
    context.called_it = False

    reporter.report_result(context, [failing_before], it_block)

    expect(context.called_it).to_be(False)


def test__report_end_result__when_a_test_has_failed__it_raises_test_failed():
    reporter = PyneDotReporter(fake_print)
    context = test_collection.top_level_describe.context

    def failing_method(self):
        expect(True).to_be(False)

    it_block = ItBlock(test_collection.top_level_describe, "some_test_name", failing_method)
    reporter.report_result(context, [], it_block)

    expect(reporter.report_end_result).to_raise_error_message("Tests failed.")


def test__report_end_result__when_all_tests_passed__it_prints_success():
    reporter = PyneDotReporter(fake_print)
    context = test_collection.top_level_describe.context

    def passing_method(self):
        pass

    it_block = ItBlock(test_collection.top_level_describe, "some_test_name", passing_method)
    reporter.report_result(context, [], it_block)
    printed_text.clear()

    reporter.report_end_result()

    expect(printed_text[0]).to_be("Success!")


def test__report_end_result__when_no_tests_run__raises_an_error():
    reporter = PyneDotReporter(fake_print)

    expect(reporter.report_end_result).to_raise_error_message("No tests to run!")
