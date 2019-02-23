
# Local Setup

## Install Dependencies

```bash
pip install pipenv
pipenv install --dev
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

Alternatively: 
```bash
python -m pyne.cli
```

# TODO

- better readability on tests with lots of commandline output
- installable cli
- cli options around focusing
- behave well around re-spying
- let pyne take method reference
