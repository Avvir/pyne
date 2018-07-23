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

To run pyne tests, you can use the cli:
```bash
./pyne/cli.py
```

For instructions on how to contribute to Pyne, read [CONTRIBUTING.md](CONTRIBUTING.md)