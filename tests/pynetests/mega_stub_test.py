from pynetest.expectations import expect
from pynetest.pyne_test_collector import describe, it, before_each, fit
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.attached_spy import AttachedSpy, attach_stub
from pynetest.test_doubles.spy import Spy
from pynetest.test_doubles.stub import MegaStub, stub, group_stubs, mega_stub


class A:
    def some_method(self):
        return "original_value_a"

class B:
    def some_method(self):
        return "original_value_b"


class TestContext:
    obj_a: A
    obj_b: B
    stub_a: Spy
    stub_b: AttachedSpy
    mega_stub: MegaStub


@pyne
def mega_stub_test():
    @before_each
    def _(self):
        tc = self.test_context = TestContext()
        tc.obj_a = A()
        tc.obj_b = B()
        tc.stub_a = attach_stub(tc.obj_a, "some_method").then_return("stubbed_value_a")
        tc.stub_b = attach_stub(tc.obj_b, "some_method").then_return("stubbed_value_b")
        tc.mega_stub = MegaStub(tc.stub_a, tc.stub_b)

    @describe("when a mega stub is created from a collection of unapplied stubs")
    def _():
        @it("does not apply the stubs")
        def _(self):
            tc: TestContext = self.test_context
            expect(tc.obj_a.some_method()).to_be("original_value_a")
            expect(tc.obj_b.some_method()).to_be("original_value_b")

    @describe("#stub")
    def _():
        @it("it applies all the stubs")
        def _(self):
            tc: TestContext = self.test_context
            tc.mega_stub.stub()
            expect(tc.obj_a.some_method()).to_be("stubbed_value_a")
            expect(tc.obj_b.some_method()).to_be("stubbed_value_b")


    @describe("#unstub")
    def _():
        @it("it removes all the stubs")
        def _(self):
            tc: TestContext = self.test_context
            tc.mega_stub.stub()
            tc.mega_stub.unstub()
            expect(tc.obj_a.some_method()).to_be("original_value_a")
            expect(tc.obj_b.some_method()).to_be("original_value_b")

    @describe("when used in a with statement")
    def _():
        @it("applies the stubs on enter and removes the stubs on exit")
        def _(self):
            tc: TestContext = self.test_context
            with tc.mega_stub:
                expect(tc.obj_a.some_method()).to_be("stubbed_value_a")
                expect(tc.obj_b.some_method()).to_be("stubbed_value_b")
            expect(tc.obj_a.some_method()).to_be("original_value_a")
            expect(tc.obj_b.some_method()).to_be("original_value_b")

    @describe("when a Spy is in the collection")
    def _():
        @before_each
        def _(self):
            tc: TestContext = self.test_context
            tc.stub_a = stub(tc.obj_a.some_method).then_return("stubbed_value_a")
            tc.stub_b = attach_stub(tc.obj_b, "some_method").then_return("stubbed_value_b")
            tc.mega_stub = mega_stub(tc.stub_a, tc.stub_b)

        @it("doesn't crash on the initial stub")
        def _(self):
            tc: TestContext = self.test_context
            tc.mega_stub.stub()
            expect(tc.obj_a.some_method()).to_be("stubbed_value_a")

        @it("is unstubbed by a call to unstub")
        def _(self):
            tc: TestContext = self.test_context
            tc.mega_stub.stub()
            tc.mega_stub.unstub()
            expect(tc.obj_a.some_method()).to_be("original_value_a")

        @it("is works when is unstubbed, then stubbed again via method calls")
        def _(self):
            tc: TestContext = self.test_context
            tc.mega_stub.stub()
            tc.mega_stub.unstub()
            tc.mega_stub.stub()
            expect(tc.obj_a.some_method()).to_be("stubbed_value_a")

        @it("is works when is unstubbed, then stubbed again via with-statement")
        def _(self):
            tc: TestContext = self.test_context
            with tc.mega_stub:
                expect(tc.obj_a.some_method()).to_be("stubbed_value_a")
            expect(tc.obj_a.some_method()).to_be("original_value_a")
            with tc.mega_stub:
                expect(tc.obj_a.some_method()).to_be("stubbed_value_a")
            expect(tc.obj_a.some_method()).to_be("original_value_a")


