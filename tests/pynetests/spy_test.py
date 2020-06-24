from pynetest.expectations import expect
from pynetest.pyne_test_collector import it, describe, fit, fdescribe, xit
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.spy import Spy
from pynetest.test_doubles.stub import stub
from tests.test_helpers import some_class
from tests.test_helpers.some_class import SomeClass

class SomeOtherClass:
    def some_function(*args, **kwargs):
        return "some_value"


@pyne
def spy_test():
    @describe("When introspection fails and method can't be found on the parent object")
    def _():
        @describe("When a decorated bound class method is spied on")
        def _():
            @it("raises a value error")
            def _(self):
                some_instance = SomeClass()
                expect(lambda: stub(some_instance.some_decorated_method)).to_raise_error_of_type(ValueError)

        @it("raises a value error")
        def _(self):
            some_instance = SomeClass()

            def some_function(*args, **kwargs):
                return "some_value"

            some_instance.some_function = some_function
            expect(lambda: stub(some_instance.some_function)).to_raise_error_of_type(ValueError)

        @describe("When a unbound class method is spied on without using 'on'")
        def _():
            @it("raises a value error")
            def _(self):
                expect(lambda: stub(SomeClass.some_method)).to_raise_error_of_type(ValueError)

        @describe("When a static method is spied on without using 'on'")
        def _():
            @it("raises a value error")
            def _(self):
                expect(lambda: stub(SomeClass.some_static_method)).to_raise_error_of_type(ValueError)

        @describe("When a unbound class method is spied on")
        def _():
            @it("raises a value error")
            def _(self):
                expect(lambda: stub(SomeClass.some_method)).to_raise_error_of_type(ValueError)

    @describe("When a spied method is called")
    def _():
        @it("tracks the arguments of the last call, clearing it on unstub")
        def _(self):
            some_instance = SomeClass()
            with stub(some_instance.some_method) as spy:
                some_instance.some_method("anything", ["can"], go="here")
                expect(spy.last_call).to_be((("anything", ["can"]), {"go": "here"}))

        @it("the last call arguments are cleared after it is unstubbed")
        def _(self):
            some_instance = SomeClass()
            with stub(some_instance.some_method) as spy:
                some_instance.some_method("anything", ["can"], go="here")
                expect(spy.last_call).to_be((("anything", ["can"]), {"go": "here"}))
            expect(spy.last_call).to_be_none()

        @it("restores the original method after it is unstubbed")
        def _(self):
            some_instance = SomeOtherClass()
            original_function = some_instance.some_function
            with stub(some_instance.some_function) as spy:
                some_instance.some_function("anything", ["can"], go="here")
                expect(spy.last_call).to_be((("anything", ["can"]), {"go": "here"}))
            expect(spy.last_call).to_be_none()
            expect(some_instance.some_function).to_be(original_function)

    @describe("When a spied method used with then_return is called")
    def _():
        @it("returns the given value")
        def _(self):
            some_instance = SomeClass()
            with stub(some_instance.some_method).then_return("some_value") as spy:
                result = some_instance.some_method("anything", ["can"], go="here")
                expect(result).to_be("some_value")

        @it("returns None after it is unstubbed")
        def _(self):
            some_instance = SomeClass()
            with stub(some_instance.some_method).then_return("some_value") as spy:
                result = some_instance.some_method("anything", ["can"], go="here")
                expect(result).to_be("some_value")
            result = some_instance.some_method("anything", ["can"], go="here")
            expect(result).to_be(None)

    @describe("When a spied method used with call_real is called")
    def _():
        @it("calls the original method and returns its value")
        def _(self):
            some_instance = SomeOtherClass()

            with stub(some_instance.some_function).call_real():
                result = some_instance.some_function("anything", ["can"], go="here")
                expect(result).to_be("some_value")

        @it("doesn't call the original method after it is unstubbed")
        def _(self):
            some_instance = SomeOtherClass()
            with stub(some_instance.some_function).call_real():
                result = some_instance.some_function("anything", ["can"], go="here")
                expect(result).to_be("some_value")

    @describe("#get_spy")
    def _():

        @describe("When a bound class method is spied on")
        def _():
            @it("can track the calls and return the spy")
            def _(self):
                some_instance = SomeClass()
                with stub(some_instance.some_method) as spy:
                    some_instance.some_method("some_arg")
                    expect(spy.last_call).to_be((("some_arg",), {}))
                    expect(Spy.get_spy(some_instance.some_method)).to_be(spy)

            @describe("when the name of the method is passed in instead of the method reference")
            def _():

                @it("can track the calls and return the spy")
                def _(self):
                    some_instance = SomeClass()
                    with stub('some_method', on=some_instance) as spy:
                        some_instance.some_method("some_arg 123")
                        expect(spy.last_call).to_be((("some_arg 123",), {}))
                        expect(Spy.get_spy(some_instance.some_method)).to_be(spy)

        @describe("When a static method is spied on")
        def _():
            @it("can track the calls and return the spy")
            def _(self):
                with stub(SomeClass.some_static_method, on=SomeClass) as spy:
                    SomeClass.some_static_method("anything", ["can"], go="here")
                    expect(spy.last_call).to_be((("anything", ["can"]), {"go": "here"}))
                    expect(Spy.get_spy(SomeClass.some_static_method)).to_be(spy)

        @describe("When a class method is spied on")
        def _():
            @it("can track the calls and return the spy")
            def _(self):
                with stub(SomeClass.some_class_method) as spy:
                    SomeClass.some_class_method("anything", ["can"], go="here")
                    expect(spy.last_call).to_be((("anything", ["can"]), {"go": "here"}))
                    expect(Spy.get_spy(SomeClass.some_class_method)).to_be(spy)

        @describe("When a module method is spied on")
        def _():
            @it("can track the calls and return the spy")
            def _(self):
                with stub(some_class.some_module_method, on=some_class) as spy:
                    some_class.some_module_method("anything", ["can"], go="here")
                    expect(spy.last_call).to_be((("anything", ["can"]), {"go": "here"}))
                    expect(Spy.get_spy(some_class.some_module_method)).to_be(spy)


