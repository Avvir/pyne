from pynetest.test_doubles.sandbox import Sandbox
from tests.test_helpers.some_class import SomeClass


def test__sandbox_spies():
    sandbox = Sandbox()
    some_class_instance = SomeClass()
    sandbox.spy(some_class_instance.some_method)
    assert len(sandbox._spies) == 1


def test__sandbox_restore():
    sandbox = Sandbox()
    some_class_instance = SomeClass()
    some_other_instace = SomeClass()
    sandbox.spy(some_class_instance.some_method)
    sandbox.spy(some_other_instace.some_positional_args_method)

    some_class_instance.some_method()
    assert sandbox._spies[0].method_name == 'some_method'
    assert sandbox._spies[1].method_name == 'some_positional_args_method'

    sandbox.restore()
    assert len(sandbox._spies) == 0


def test__sandbox_reset():
    sandbox = Sandbox()
    some_class_instance = SomeClass()
    sandbox.spy(some_class_instance.some_method)

    some_class_instance.some_method("some_arg")
    assert some_class_instance.some_method.last_call == (("some_arg",), {})
    sandbox.reset()
    assert some_class_instance.some_method.last_call is None


def test__sandbox_when_calling_then_return():
    sandbox = Sandbox()
    some_class_instance = SomeClass()
    sandbox.when_calling(some_class_instance.some_method).then_return(5)
    assert some_class_instance.some_method() == 5


