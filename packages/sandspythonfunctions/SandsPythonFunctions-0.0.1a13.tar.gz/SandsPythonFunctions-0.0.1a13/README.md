# Sands Python Functions

Some functions I find useful regularly and I put them all into one package for easy access

I created this using [Poetry](https://python-poetry.org/).

## Instructions

- To build this you must first install poetry see instructions [here](https://python-poetry.org/docs/#installation)
- However to make it easy to access this is all of the code you'll need on linux to make this run (note that I use zsh not bash for my shell)
    - First you must navigate to the folder containing these files `CHANGELOG.md   LICENSE  'README reference.md'   README.md   dist   poetry.lock   pyproject.toml   src`
    - You then to make sure that you have the python environment that you want activated
    - You can then enter the code below

```sh
poetry build
poetry install
```

## Basic Usage Example

TODO:

## Included Packages

### Functions from EmailFunctions

- 

### Functions from MultiprocessingFunctions

- 

### Functions from ParquetFunctions

- 

### Functions from PrintFunctions

- 

### Functions from TimerFunctions

- 

## Testing

Pytest runs in whatever directory you're located in at the time you run pytest so if you're not in the directory of the test scripts pytest will not see the files it needs to and will then fail.

Follow the code below to test the functions

```sh
cd src/tests
pytest /src/tests/EmailFunctions_test.py
pytest /src/tests/MultiprocessingFunctions_test.py
pytest /src/tests/ParquetFunctions_test.py
```

## CI/CD

See [this repo](https://github.com/speg03/shishakai/blob/971261e6f73ee8b9dcc83837b6c1a5f809c985f8/.github/workflows/upload-python-package.yml) for an example of someone using poetry with they're python project to upload to PyPI on push to master.
