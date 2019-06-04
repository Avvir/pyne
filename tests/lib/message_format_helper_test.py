from pynetest.expectations import expect
from pynetest.lib.message_format_helper import format_object, format_arguments
from tests.test_helpers.some_class import SomeClass


def test__message_format_helper__format_object__can_format_functions():
    expect(format_object(SomeClass.some_method)).to_be("tests.test_helpers.some_class.some_method")

def test__message_format_helper__format_object__can_format_curly_braces():
    expect(format_object({1:2})).to_be("{{1: 2}}")

def test__message_format_helper__format_arguments__can_format_curly_braces():
    expect(format_arguments([{1:2}])).to_be("({{1: 2}})")
