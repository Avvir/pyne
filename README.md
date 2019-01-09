# Pyne Testing Framework

Pyne is a BDD style testing framework for Python. It's styled after frameworks for other languages like Mocha, Jasmine, Spectrum, and Rspec.

An example pyne test:
```python
@pyne
def some_file():
    @describe("when two numbers are added together")
    def _():
      @before_each
      def _(self):
        self.calculator = Calculator()

      @it("returns the sum")
      def _(self):
        expect(self.calculator.calculate("22 + 11")).to_be(33)
```
You can see more examples in the [examples folder](./examples)

## Running tests
### Run a file

```bash
python some_test.py
```

### Run all tests

To run all the tests in a directory, you can use the cli:
```bash
./pyne/cli.py
```

### Run only some tests

You can focus on a single test by using `@fit` instead of `@it`
Or a single describe block by using `@fdescribe` instead of `@describe`

## Using Test Doubles
### Spying

In order to spy on an instances methods:

```python
from pyne.expectations import expect
from pyne.pyne_test_collector import before_each, describe, it
from pyne.test_doubles.spy import stub

from some_module import SomeClass

@describe("SomeClass")
def _():
    @before_each
    def _(self):
        self.class_instance = SomeClass()
        stub(self.class_instance, self.class_instance.some_method)
    
    @it("gets called with something")
    def _(self):
        self.class_instance.some_method("something")
        expect(self.class_instance.some_method).was_called_with("something")
```

If you need the method to still return something, you scan specify what it returns:

```python
    @before_each
    def _(self):
        self.class_instance = SomeClass()
        stub(self.class_instance, self.class_instance.some_method)
        self.class_instance.some_method.returns("some value")
```
# Contribution / Development

For instructions on how to contribute to Pyne, read [CONTRIBUTING.md](CONTRIBUTING.md)
