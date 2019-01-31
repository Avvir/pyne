#!/usr/bin/env bash

pipenv run pytest tests  && PYTHONPATH=. pipenv run python pyne/cli.py tests/pynetests