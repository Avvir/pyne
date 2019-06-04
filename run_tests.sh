#!/usr/bin/env bash

pipenv run pytest tests  && PYTHONPATH=. pipenv run python pynetest/cli.py tests/pynetests