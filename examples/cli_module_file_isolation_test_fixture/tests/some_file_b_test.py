import sys

from pyne.expectations import expect
from pyne.pyne_test_collector import it
from pyne.pyne_tester import pyne


from tests.test_helpers.test_modules import some_module_in_file_b, some_shared_module


@pyne
def some_second_file_test():
    @it("has all the modules from b")
    def _(self):
        from tests.test_helpers.test_modules import some_module_in_it_b
        loaded_modules_with_some = { name: module for (name, module) in sys.modules.items() if "some" in name }
        expect(loaded_modules_with_some).to_contain("tests.test_helpers.test_modules.some_module_in_file_b")
        expect(loaded_modules_with_some).to_contain("tests.test_helpers.test_modules.some_module_in_it_b")

    @it("has no modules from a")
    def _(self):
        loaded_modules_with_some = { name: module for (name, module) in sys.modules.items() if "some" in name }
        expect(loaded_modules_with_some).not_to_contain("tests.test_helpers.test_modules.some_module_in_file_a")
        expect(loaded_modules_with_some).not_to_contain("tests.test_helpers.test_modules.some_module_in_it_a")

    @it("shared module has changes from b and not a")
    def _(self):
        some_shared_module.default_false_set_true_by_b = True
        expect(some_shared_module.default_false_set_true_by_b).to_be(True)
        expect(some_shared_module.default_false_set_true_by_a).to_be(False)
