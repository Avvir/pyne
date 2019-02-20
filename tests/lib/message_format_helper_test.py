from pyne.expectations import expect
from pyne.lib.message_format_helper import format_object
from tests.test_helpers.some_class import SomeClass


def test__message_format_helper__format_object__can_format_functions():
    expect(format_object(SomeClass.some_method)).to_be("tests.test_helpers.some_class.some_method")
