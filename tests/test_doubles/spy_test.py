from pyne.test_doubles.spy import Spy
from pyne.test_doubles.stub import stub
from tests.test_helpers.some_class import SomeClass
from tests.test_helpers.temporary_class import TemporaryClass


def test__tracks_what_it_was_called_with():
    spy = Spy()

    spy("anything", ["can"], go="here")
    assert spy.last_call == (("anything", ["can"]), {"go": "here"})


def test__returns__returns_the_given_value_when_the_spy_is_called():
    spy = Spy()

    spy.returns("some value")
    assert spy("anything", ["can"], go="here") == "some value"


def test__restore__resets_what_the_spy_was_last_called_with():
    spy = Spy()

    spy("anything", ["can"], go="here")
    assert spy.last_call == (("anything", ["can"]), {"go": "here"})

    spy.restore()
    assert spy.last_call is None


def test__restore__causes_the_spy_to_return_none():
    spy = Spy()

    spy.returns("some value")
    assert spy("anything", ["can"], go="here") == "some value"

    spy.restore()
    assert spy("anything", ["can"], go="here") is None


def test__when_passed_in_an_instance_and_instance_method__tracks_what_the_method_was_called_with():
    instance = SomeClass()
    stub(instance, instance.some_method)

    instance.some_method("anything", ["can"], go="here")
    assert instance.some_method.last_call == (("anything", ["can"]), {"go": "here"})


def test__when_passed_in_an_instance_and_instance_method__returns__returns_the_given_value_when_the_stubbed_method_is_called():
    instance = SomeClass()
    stub(instance, instance.some_method).returns("some value")

    assert instance.some_method("anything", ["can"], go="here") == "some value"


def test__when_passed_in_an_instance_and_instance_method__restore__sets_the_method_back_to_what_it_originally_was():
    instance = SomeClass()
    stub(instance, instance.some_method).returns("some value")

    assert instance.some_method("anything", ["can"], go="here") == "some value"

    instance.some_method.restore()
    assert instance.some_method("anything", ["can"], go="here") is None


def test__when_passed_in_an_class_and_static_method__tracks_what_the_method_was_called_with():
    with TemporaryClass() as SomeTemporaryClass:
        stub(SomeTemporaryClass, SomeTemporaryClass.some_static_method)

        SomeTemporaryClass.some_static_method("anything", ["can"], go="here")
        assert SomeTemporaryClass.some_static_method.last_call == (("anything", ["can"]), {"go": "here"})


def test__when_passed_in_an_class_and_static_method__returns__returns_the_given_value_when_the_stubbed_method_is_called():
    with TemporaryClass() as SomeTemporaryClass:
        stub(SomeTemporaryClass, SomeTemporaryClass.some_static_method).returns("some value")

        assert SomeTemporaryClass.some_static_method("anything", ["can"], go="here") == "some value"


def test__when_passed_in_an_class_and_static_method__restore__sets_the_method_back_to_what_it_originally_was():
    stub(SomeClass, SomeClass.some_static_method).returns("some value")

    assert SomeClass.some_static_method("anything", ["can"], go="here") == "some value"

    SomeClass.some_static_method.restore()
    assert SomeClass.some_static_method("anything", ["can"], go="here") is None
