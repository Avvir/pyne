from pyne.expectations import expect
from pyne.pyne_test_collector import it
from pyne.pyne_tester import pyne
import sys
from tests.test_helpers.test_modules import some_module_in_file_a
from tests.test_helpers.test_modules import some_shared_module


@pyne
def some_first_file_test():
    from tests.test_helpers.test_modules import some_module_in_pyne_a

    @it("can pass")
    def _(self):
        pass

    @it("has all the modules from a")
    def _(self):
        from tests.test_helpers.test_modules import some_module_in_it_a
        loaded_modules_with_some = { name: module for (name, module) in sys.modules.items() if "some" in name }
        expect(loaded_modules_with_some).to_contain("tests.test_helpers.test_modules.some_module_in_file_a")
        expect(loaded_modules_with_some).to_contain("tests.test_helpers.test_modules.some_module_in_pyne_a")
        expect(loaded_modules_with_some).to_contain("tests.test_helpers.test_modules.some_module_in_it_a")

    @it("has no modules from b")
    def _(self):
        loaded_modules_with_some = { name: module for (name, module) in sys.modules.items() if "some" in name }
        expect(loaded_modules_with_some).not_to_contain("tests.test_helpers.test_modules.some_module_in_file_b")
        expect(loaded_modules_with_some).not_to_contain("tests.test_helpers.test_modules.some_module_in_pyne_b")
        expect(loaded_modules_with_some).not_to_contain("tests.test_helpers.test_modules.some_module_in_it_b")

    @it("shared module has changes from a and not b")
    def _(self):
        some_shared_module.default_false_set_true_by_a = True
        expect(some_shared_module.default_false_set_true_by_a).to_be(True)
        expect(some_shared_module.default_false_set_true_by_b).to_be(False)
