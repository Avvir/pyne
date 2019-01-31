from pyne.test_doubles.spy import stub
from tests.test_helpers.some_class import SomeClass


def test__returns__returns_the_given_value_when_the_stubbed_method_is_called():
    instance = SomeClass()
    stub(instance, instance.some_method)
    instance.some_method.returns("some value")
    assert instance.some_method("anything", ["can"], go="here") == "some value"
