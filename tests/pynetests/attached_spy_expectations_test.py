from pynetest.expectations import expect
from pynetest.pyne_test_collector import it, describe
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.attached_spy import AttachedSpy, attach_spy
from tests.pynetests.expectations_test import expect_assertion_error
from tests.test_helpers import some_class
from tests.test_helpers.some_class import SomeClass


@pyne
def attached_spy_expectations_test():
    @describe("#was_called")
    def _():
        @it("it passes if the method is called")
        def _(self):
            some_instance = SomeClass()
            with attach_spy(some_instance, "some_method"):
                some_instance.some_method()
                expect(some_instance.some_method).was_called()

        @it("it fails if the method is not called")
        def _(self):
            some_instance = SomeClass()
            with attach_spy(some_instance, "some_method"):
                expect_assertion_error(lambda: expect(some_instance.some_method).was_called())

        @it("it fails if the method is not tracked")
        def _(self):
            some_instance = SomeClass()
            expect_assertion_error(lambda: expect(some_instance.some_method).was_called())

        @describe("When a unbound class method is spied on")
        def _():
            @it("it passes if the method is called")
            def _(self):
                with AttachedSpy(SomeClass, "some_method"):
                    some_instance = SomeClass()
                    some_instance.some_method("some_arg")
                    expect(some_instance.some_method).was_called()

        @describe("When a bound class method is spied on")
        def _():
            @it("it passes if the method is called")
            def _(self):
                with AttachedSpy(SomeClass, "some_method"):
                    some_instance = SomeClass()
                    some_instance.some_method("some_arg")
                    expect(some_instance.some_method).was_called()

        @describe("When a decorated bound class method is spied on")
        def _():
            @it("it passes if the method is called")
            def _(self):
                some_instance = SomeClass()
                with AttachedSpy(some_instance, "some_decorated_method"):
                    some_instance.some_decorated_method("anything", ["can"], go="here")
                    expect(some_instance.some_decorated_method).was_called()

        @describe("When a static method is spied on")
        def _():
            @it("it passes if the method is called")
            def _(self):
                with AttachedSpy(SomeClass, "some_static_method"):
                    SomeClass.some_static_method("anything", ["can"], go="here")
                    expect(SomeClass.some_static_method).was_called()

        @describe("When a class method is spied on")
        def _():
            @it("it passes if the method is called")
            def _(self):
                with AttachedSpy(SomeClass, "some_class_method"):
                    SomeClass.some_class_method("anything", ["can"], go="here")
                    expect(SomeClass.some_class_method).was_called()

        @describe("When a module method is spied on")
        def _():
            @it("it passes if the method is called")
            def _(self):
                with AttachedSpy(some_class, "some_module_method"):
                    some_class.some_module_method("anything", ["can"], go="here")
                    expect(some_class.some_module_method).was_called()

    @describe("#was_not_called")
    def _():
        @it("it passes if the method is not called")
        def _(self):
            some_instance = SomeClass()
            with attach_spy(some_instance, "some_method"):
                expect(some_instance.some_method).was_not_called()

        @it("it fails if the method is called")
        def _(self):
            some_instance = SomeClass()
            with attach_spy(some_instance, "some_method"):
                some_instance.some_method()
                expect_assertion_error(lambda: expect(some_instance.some_method).was_not_called())

        @it("it fails if the method is not tracked")
        def _(self):
            some_instance = SomeClass()
            expect_assertion_error(lambda: expect(some_instance.some_method).was_not_called())

        @describe("When a unbound class method is spied on")
        def _():
            @it("it passes if the method is not called")
            def _(self):
                with AttachedSpy(SomeClass, "some_method"):
                    some_instance = SomeClass()
                    expect(some_instance.some_method).was_not_called()

        @describe("When a bound class method is spied on")
        def _():
            @it("it passes if the method is not called")
            def _(self):
                with AttachedSpy(SomeClass, "some_method"):
                    some_instance = SomeClass()
                    expect(some_instance.some_method).was_not_called()

        @describe("When a decorated bound class method is spied on")
        def _():
            @it("it passes if the method is not called")
            def _(self):
                some_instance = SomeClass()
                with AttachedSpy(some_instance, "some_decorated_method"):
                    expect(some_instance.some_decorated_method).was_not_called()

        @describe("When a static method is spied on")
        def _():
            @it("it passes if the method is not called")
            def _(self):
                with AttachedSpy(SomeClass, "some_static_method"):
                    expect(SomeClass.some_static_method).was_not_called()

        @describe("When a class method is spied on")
        def _():
            @it("it passes if the method is not called")
            def _(self):
                with AttachedSpy(SomeClass, "some_class_method"):
                    expect(SomeClass.some_class_method).was_not_called()

        @describe("When a module method is spied on")
        def _():
            @it("it passes if the method is not called")
            def _(self):
                with AttachedSpy(some_class, "some_module_method"):
                    expect(some_class.some_module_method).was_not_called()


    @describe("#was_called_with")
    def _():
        @it("it passes if the method is called with the args")
        def _(self):
            some_instance = SomeClass()
            with attach_spy(some_instance, "some_method"):
                expect(some_instance.some_method).was_not_called()
                some_instance.some_method("anything", ["can"], go="here")
                expect(some_instance.some_method).was_called_with("anything", ["can"], go="here")
