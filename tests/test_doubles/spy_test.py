from pynetest.expectations import expect
from pynetest.test_doubles.spy import Spy

from pynetest.test_doubles.stub import when, spy_on, group_stubs
from tests.test_helpers.some_class import SomeClass
from tests.test_helpers.temporary_class import TemporaryClass

Spy._validate_spy = False


def test__tracks_what_it_was_called_with():
    spy = Spy()

    spy("anything", ["can"], go="here")
    assert spy.last_call == (("anything", ["can"]), {"go": "here"})


def test__tracks_calls():
    spy = Spy()
    spy("arg1", kwarg1="kwarg1")
    spy("arg2", kwarg2="kwarg2")
    assert spy.calls[0] == (("arg1",), {"kwarg1": "kwarg1"})
    assert spy.calls[1] == (("arg2",), {"kwarg2": "kwarg2"})


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


def test__exit__calls_when_with_statement_is_exited():
    with Spy() as spy:
        spy("anything", ["can"], go="here")
        expect(spy.last_call).to_be((("anything", ["can"]), {"go": "here"}))
    expect(spy.last_call).to_be_none()


def test__stub__when_passed_in_an_instance_method__tracks_what_the_method_was_called_with():
    instance = SomeClass()
    spy = when(instance.some_method)

    instance.some_method("anything", ["can"], go="here")
    expect(spy.last_call).to_be((("anything", ["can"]), {"go": "here"}))


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


def test__stub__when_stubbing_a_class_method__tracks_what_the_method_was_called_with():
    with TemporaryClass() as SomeTemporaryClass:
        when(SomeTemporaryClass.some_class_method, SomeTemporaryClass)

        SomeTemporaryClass.some_class_method("anything", ["can"], go="here")
        expect(SomeTemporaryClass.some_class_method.last_call).to_be((("anything", ["can"]), {"go": "here"}))


def test__then_return__can_set_the_return_value_for_a_class_method():
    with TemporaryClass() as SomeTemporaryClass:
        when(SomeTemporaryClass.some_class_method).then_return("some value")

        expect(SomeTemporaryClass.some_class_method("anything", ["can"], go="here")).to_be("some value")


def test__restore__can_set_a_class_method_back_to_what_it_originally_was():
    with TemporaryClass() as SomeTemporaryClass:
        original_class_method = SomeTemporaryClass.some_class_method

        when(SomeTemporaryClass.some_class_method).then_return("some value")

        SomeTemporaryClass.some_class_method.restore()

        expect(SomeTemporaryClass.some_class_method).to_be(original_class_method)


def test__stub__when_spying_on_a_function__tracks_what_the_method_was_called_with():
    def some_function(*args, **kwargs):
        return "some_value"

    with spy_on(some_function) as spy:
        spy("anything", ["can"], go="here")
        expect(spy.last_call).to_be((("anything", ["can"]), {"go": "here"}))


def test__stub__when_spying_on_a_function_with_call_real__tracks_what_the_real_method_returns():
    def some_function(*args, **kwargs):
        return "some_value"

    with spy_on(some_function).call_real() as spy:
        spy("anything", ["can"], go="here")
        expect(spy.return_value).to_be("some_value")


def test__stub__when_spying_on_a_function__tracks_what_the_stubbed_method_returns():
    def some_function(*args, **kwargs):
        return "some_value"

    with spy_on(some_function) as spy:
        spy("anything", ["can"], go="here")
        expect(spy.return_value).to_be(None)


def test__then_return__can_set_the_return_value_for_a_function():
    def some_function(*args, **kwargs):
        return "some_value"

    with when(some_function) as spy:
        spy.then_return("some_other_value")
        expect(spy.return_value).to_be("some_other_value")


def test__when_calling_group__calls_all_exits_on_group_restore():
    with TemporaryClass() as SomeTemporaryClass:
        some_instance = SomeTemporaryClass()

        original_method_a = some_instance.some_method
        original_method_b = some_instance.some_other_method

        group = group_stubs(spy_on(some_instance.some_method),
                            spy_on(some_instance.some_other_method))

        expect(some_instance.some_method).not_to_be(original_method_a)
        expect(some_instance.some_other_method).not_to_be(original_method_b)

        group.restore()

        expect(some_instance.some_method).to_be(original_method_a)
        expect(some_instance.some_other_method).to_be(original_method_b)


def test__when_calling_group__calls_all_exits_on_group_exit():
    with TemporaryClass() as SomeTemporaryClass:
        some_instance = SomeTemporaryClass()

        original_method_a = some_instance.some_method
        original_method_b = some_instance.some_other_method

        group = group_stubs(spy_on(some_instance.some_method),
                            spy_on(some_instance.some_other_method))

        with group:
            expect(some_instance.some_method).not_to_be(original_method_a)
            expect(some_instance.some_other_method).not_to_be(original_method_b)

        expect(some_instance.some_method).to_be(original_method_a)
        expect(some_instance.some_other_method).to_be(original_method_b)
