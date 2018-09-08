# python-tia

[![PyPI version](https://badge.fury.io/py/python-tia.svg)](https://badge.fury.io/py/python-tia)
[![GitHub license](https://img.shields.io/github/license/fkromer/python-tia.svg)](https://github.com/fkromer/python-tia/blob/master/LICENSE)
[![Read the Docs](https://img.shields.io/readthedocs/pip.svg)](https://python-tia.readthedocs.io)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/fkromer)

`tia`: The generic Test Impact Analysis (TIA) preprocessor for test tools.

## Installation

    $ pip3 install --user python-tia

## Documentation

Refer to the documentation on [python-tia.readthedocs.io](https://python-tia.readthedocs.io).

## Development

Install development requirements from `Pipfile`:

    $ pipenv install --skip-lock

Show available `tox` environments:

    $ pipenv run tox -av

Run `tox` environments (here: `docs`):

    $ pipenv run tox -e docs