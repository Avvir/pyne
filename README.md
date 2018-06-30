# Pyne Testing Framework

Pyne is a BDD style testing framework for Python. It's styled after frameworks for other languages like Mocha, Jasmine, Spectrum, and Rspec.

An example pyne test:
```python

@describe
def when_two_numbers_are_added_together():
  @before_each
  def do(self):
    self.calculator = new Calculator()

  @it
  def returns_the_sum(self):
    expect(self.calculator.calculate("22 + 11")).to_be(33)
```

# Local Setup

## Install Dependencies

```bash
pip install pipenv
pipenv install
```

## Test

```bash
pipenv run pytest
```