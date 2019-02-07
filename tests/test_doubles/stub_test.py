from pyne.test_doubles.spy import Spy
from pyne.test_doubles.stub import stub
from tests.test_helpers.some_class import SomeClass


def test__returns_the_spy_for_the_stubbed_method():
    some_instance = SomeClass()
    some_method = some_instance.some_method
    spy = stub(some_instance, some_instance.some_method)

    assert isinstance(spy, Spy)
    assert spy.stubbed_object == some_instance
    assert spy.method == some_method
