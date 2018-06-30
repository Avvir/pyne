from pyne.expectations import expect
from pyne.pyne_test_blocks import ItBlock


def test_when_a_test_fails__it_prints_an_x():
    it_block = ItBlock(None, "some_test_name", expect(True).to_be(False))
    # report_it_result(method_to_run, behavior_description, ancestors_description, behavior)