from pyne.expectations import expect
from pyne.test_doubles.spy import Spy

from pyne.test_doubles.when_calling import when
from tests.test_helpers.some_class import SomeClass
from tests.test_helpers.temporary_class import TemporaryClass


def test__tracks_what_it_was_called_with():
    spy = Spy()

    spy("anything", ["can"], go="here")
    assert spy.last_call == (("anything", ["can"]), {"go": "here"})


def test__then_return__returns_the_given_value_when_the_spy_is_called():
    spy = Spy()

    spy.then_return("some value")
    expect(spy("anything", ["can"], go="here")).to_be("some value")


def test__restore__resets_what_the_spy_was_last_called_with():
    spy = Spy()

    spy("anything", ["can"], go="here")
    expect(spy.last_call).to_be((("anything", ["can"]), {"go": "here"}))

    spy.restore()
    expect(spy.last_call).to_be_none()


def test__restore__causes_the_spy_to_return_none():
    spy = Spy()

    spy.then_return("some value")
    expect(spy("anything", ["can"], go="here")).to_be("some value")

    spy.restore()
    expect(spy("anything", ["can"], go="here")).to_be_none()


def test__stub__when_passed_in_an_instance_method__tracks_what_the_method_was_called_with():
    instance = SomeClass()
    when(instance.some_method)

    instance.some_method("anything", ["can"], go="here")
    expect(instance.some_method.last_call).to_be((("anything", ["can"]), {"go": "here"}))


def test__then_return__returns_the_given_value_when_a_stubbed_method_is_called():
    instance = SomeClass()

    when(instance.some_method).then_return("some value")

    expect(instance.some_method("anything", ["can"], go="here")).to_be("some value")


def test__restore__after_stubbing_an_instance_method__sets_the_method_back_to_what_it_originally_was():
    instance = SomeClass()
    when(instance.some_method).then_return("some value")

    instance.some_method.restore()
    expect(instance.some_method("anything", ["can"], go="here")).to_be_none()


def test__stub__when_stubbing_a_static_method__tracks_what_the_method_was_called_with():
    with TemporaryClass() as SomeTemporaryClass:
        when(SomeTemporaryClass.some_static_method, SomeTemporaryClass)

        SomeTemporaryClass.some_static_method("anything", ["can"], go="here")
        expect(SomeTemporaryClass.some_static_method.last_call).to_be((("anything", ["can"]), {"go": "here"}))


def test__then_return__can_set_the_return_value_for_a_static_method():
    with TemporaryClass() as SomeTemporaryClass:
        when(SomeTemporaryClass.some_static_method, on=SomeTemporaryClass).then_return("some value")

        expect(SomeTemporaryClass.some_static_method("anything", ["can"], go="here")).to_be("some value")


def test__restore__can_set_a_static_method_back_to_what_it_originally_was():
    with TemporaryClass() as SomeTemporaryClass:
        original_static_method = SomeTemporaryClass.some_static_method
        
        when(SomeTemporaryClass.some_static_method, on=SomeTemporaryClass).then_return("some value")

        SomeTemporaryClass.some_static_method.restore()

        expect(SomeTemporaryClass.some_static_method).to_be(original_static_method)
