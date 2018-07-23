
# Local Setup

## Install Dependencies

```bash
pip install pipenv
pipenv install
```

## Test

```bash
pipenv run pytest tests
```

## Run Example Tests

Pyne needs to be on the python path in order to use the cli:
```bash
PYTHONPATH=`pwd` ./pyne/cli.py
```