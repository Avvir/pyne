from pynetest.expectations import expect
from pynetest.pyne_test_collector import it, describe, fdescribe, fit
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.attached_spy import AttachedSpy
from pynetest.test_doubles.spy import last_call_of
from tests.test_helpers import some_class
from tests.test_helpers.some_class import SomeClass



@pyne
def atteched_spy_test():
    @describe("When the named method doesn't exist on the parent object")
    def _():
        @it("raises a value error")
        def _(self):
            some_instance = SomeClass()
            expect(lambda: AttachedSpy(some_instance, "some_nonexistent_method")).to_raise_error_of_type(ValueError)

    @describe("When a spied method is called")
    def _():
        @it("tracks the arguments of the last call, clearing it on unstub")
        def _(self):
            some_instance = SomeClass()
            with AttachedSpy(some_instance, "some_method") as spy:
                some_instance.some_method("anything", ["can"], go="here")
                expect(spy.last_call).to_be((("anything", ["can"]), {"go": "here"}))

        @it("adds the call to the calls list")
        def _(self):
            some_instance = SomeClass()
            with AttachedSpy(some_instance, "some_method") as spy:
                some_instance.some_method("anything", ["can"], go="here")
                some_instance.some_method("or", ["here"], xor="here")
                expect(spy.calls).to_have_length(2)
                expect(spy.calls[1]).to_be((("or", ["here"]), {"xor": "here"}))

        @it("the last call arguments are cleared after it is unstubbed")
        def _(self):
            some_instance = SomeClass()
            with AttachedSpy(some_instance, "some_method") as spy:
                some_instance.some_method("anything", ["can"], go="here")
                expect(spy.last_call).to_be((("anything", ["can"]), {"go": "here"}))
            expect(spy.last_call).to_be_none()

        @it("restores the original method after it is unstubbed")
        def _(self):
            def some_function(*args, **kwargs):
                return "some_value"

            some_instance = SomeClass()
            some_instance.some_function = some_function

            with AttachedSpy(some_instance, "some_function") as spy:
                some_instance.some_function("anything", ["can"], go="here")
                expect(spy.last_call).to_be((("anything", ["can"]), {"go": "here"}))
            expect(some_instance.some_function).to_be(some_function)

    @describe("When a spied method used with then_return is called")
    def _():
        @it("returns the given value")
        def _(self):
            some_instance = SomeClass()
            with AttachedSpy(some_instance, "some_method").then_return("some_value") as spy:
                result = some_instance.some_method("anything", ["can"], go="here")
                expect(result).to_be("some_value")

        @it("returns None after it is unstubbed")
        def _(self):
            some_instance = SomeClass()
            with AttachedSpy(some_instance, "some_method").then_return("some_value") as spy:
                result = some_instance.some_method("anything", ["can"], go="here")
                expect(result).to_be("some_value")
            result = some_instance.some_method("anything", ["can"], go="here")
            expect(result).to_be(None)

    @describe("When a spied method used with then_return_sequence is called")
    def _():
        @it("returns the next value in the sequence each time it is called")
        def _(self):
            some_instance = SomeClass()
            with AttachedSpy(some_instance, "some_method").then_return_sequence(("some_value", "some_value2")) as spy:
                result = some_instance.some_method("anything", ["can"], go="here")
                result2 = some_instance.some_method("anything", ["can"], go="here")
                result3 = some_instance.some_method("anything", ["can"], go="here")
                expect(result).to_be("some_value")
                expect(result2).to_be("some_value2")
                expect(result3).to_be(None)

        @it("returns None after it is unstubbed")
        def _(self):
            some_instance = SomeClass()
            with AttachedSpy(some_instance, "some_method").then_return("some_value") as spy:
                result = some_instance.some_method("anything", ["can"], go="here")
                expect(result).to_be("some_value")
            result = some_instance.some_method("anything", ["can"], go="here")
            expect(result).to_be(None)

        @describe("when then_return() is also called")
        def _():
            @describe("when there are less than or equal number of calls as return sequence values")
            def _():
                @it("returns the return sequence values")
                def _(self):
                    some_instance = SomeClass()
                    with AttachedSpy(some_instance, "some_method").then_return_sequence(["some_value", "some_value2"]).then_return('abc') as spy:
                        result = some_instance.some_method("anything", ["can"], go="here")
                        result2 = some_instance.some_method("anything", ["can"], go="here")
                        expect(result).to_be("some_value")
                        expect(result2).to_be("some_value2")

            @describe("when there are more calls than return sequence values")
            def _():
                @it("returns the return sequence values, then returns the then_return value for all future calls")
                def _(self):
                    some_instance = SomeClass()
                    with AttachedSpy(some_instance, "some_method").then_return_sequence(["some_value", "some_value2"]).then_return('abc') as spy:
                        result = some_instance.some_method("anything", ["can"], go="here")
                        result2 = some_instance.some_method("anything", ["can"], go="here")
                        result3 = some_instance.some_method("anything", ["can"], go="here")
                        result4 = some_instance.some_method("anything", ["can"], go="here")
                        expect(result).to_be("some_value")
                        expect(result2).to_be("some_value2")
                        expect(result3).to_be("abc")
                        expect(result4).to_be("abc")




    @describe("When a spied method used with call_real is called")
    def _():
        @it("calls the original method and returns its value")
        def _(self):
            some_instance = SomeClass()

            def some_function(*args, **kwargs):
                return "some_value"

            some_instance.some_function = some_function

            with AttachedSpy(some_instance, "some_function").call_real():
                result = some_instance.some_function("anything", ["can"], go="here")
                expect(result).to_be("some_value")

        @describe("When a unbound class method is spied on")
        def _():
            @it("calls the original method and returns its value")
            def _(self):
                with AttachedSpy(SomeClass, "some_args_method_that_returns_some_value", needs_binding=True).call_real() as spy:
                    some_class = SomeClass()
                    expect(some_class.some_args_method_that_returns_some_value("some_arg", some_keyword_arg="some_kwarg")).to_be("some_value")
                    expect(some_class.some_args_method_that_returns_some_value).was_called_with("some_arg", some_keyword_arg="some_kwarg")

    @describe("When a spied method used with then_call is called")
    def _():
        @it("calls the new method instead and returns its value")
        def _(self):
            some_instance = SomeClass()

            def some_function(*args, **kwargs):
                return "some_value"

            def some_other_function(*args, **kwargs):
                return "some_other_value"

            some_instance.some_function = some_function

            with AttachedSpy(some_instance, "some_function").then_call(some_other_function):
                result = some_instance.some_function("anything", ["can"], go="here")
                expect(result).to_be("some_other_value")

        @it("doesn't call the new method after it is unstubbed")
        def _(self):
            some_instance = SomeClass()

            def some_function(*args, **kwargs):
                return "some_value"

            def some_other_function(*args, **kwargs):
                return "some_other_value"

            some_instance.some_function = some_function

            with AttachedSpy(some_instance, "some_function").then_call(some_other_function):
                result = some_instance.some_function("anything", ["can"], go="here")
                expect(result).to_be("some_other_value")
            expect(some_instance.some_function()).to_be("some_value")

    @describe("#get_spy")
    def _():
        @describe("When a unbound class method is spied on")
        def _():
            @it("can track the calls of a instance and return the spy")
            def _(self):
                with AttachedSpy(SomeClass, "some_method", needs_binding=True) as spy:
                    some_instance = SomeClass()
                    some_instance.some_method("some_arg")
                    expect(spy.last_call).to_be((("some_arg",), {}))
                    expect(AttachedSpy.get_spy(some_instance.some_method)).to_be(spy)

        @describe("When a bound class method is spied on")
        def _():
            @it("can track the calls and return the spy")
            def _(self):
                some_instance = SomeClass()
                with AttachedSpy(some_instance, "some_method") as spy:
                    some_instance.some_method("some_arg")
                    expect(spy.last_call).to_be((("some_arg",), {}))
                    expect(AttachedSpy.get_spy(some_instance.some_method)).to_be(spy)

        @describe("When a decorated bound class method is spied on")
        def _():
            @it("can track the calls and return the spy")
            def _(self):
                some_instance = SomeClass()
                with AttachedSpy(some_instance, "some_decorated_method") as spy:
                    some_instance.some_decorated_method("anything", ["can"], go="here")
                    expect(spy.last_call).to_be((("anything", ["can"]), {"go": "here"}))
                    expect(AttachedSpy.get_spy(some_instance.some_decorated_method)).to_be(spy)

        @describe("When a static method is spied on")
        def _():
            @it("can track the calls and return the spy")
            def _(self):
                with AttachedSpy(SomeClass, "some_static_method") as spy:
                    SomeClass.some_static_method("anything", ["can"], go="here")
                    expect(spy.last_call).to_be((("anything", ["can"]), {"go": "here"}))
                    expect(AttachedSpy.get_spy(SomeClass.some_static_method)).to_be(spy)

        @describe("When a class method is spied on")
        def _():
            @it("can track the calls and return the spy")
            def _(self):
                with AttachedSpy(SomeClass, "some_class_method") as spy:
                    SomeClass.some_class_method("anything", ["can"], go="here")
                    expect(spy.last_call).to_be((("anything", ["can"]), {"go": "here"}))
                    expect(AttachedSpy.get_spy(SomeClass.some_class_method)).to_be(spy)

        @describe("When a module method is spied on")
        def _():
            @it("can track the calls and return the spy")
            def _(self):
                with AttachedSpy(some_class, "some_module_method") as spy:
                    some_class.some_module_method("anything", ["can"], go="here")
                    expect(spy.last_call).to_be((("anything", ["can"]), {"go": "here"}))
                    expect(AttachedSpy.get_spy(some_class.some_module_method)).to_be(spy)

    @describe("#last_call_of")
    def _():
        @it("return last_call of the underlying method spy")
        def _(self):
            some_instance = SomeClass()
            with AttachedSpy(some_instance, "some_method") as spy:
                some_instance.some_method("anything", ["can"], go="here")
                expect(last_call_of(some_instance.some_method)).to_be((("anything", ["can"]), {"go": "here"}))
