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
        self.calculator = new Calculator()

      @it("returns the sum)
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
Or a single decribe block by using `@fdescribe` instead of `@describe`


# Contribution / Development

For instructions on how to contribute to Pyne, read [CONTRIBUTING.md](CONTRIBUTING.md)