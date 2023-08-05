# REST API specification and implementation testing

Library and CLI tool for automated REST API testing.

For the test file format, see the [example tests](examples/tests.yaml)

## Installation

Requires python>=3.6

```bash
pip install apievaluator
```

For argument descriptions, see `apieval --help`

## Local development

```bash
pip instal pipenv
pipenv update
pipenv shell

apieval -s path/to/spec -u https://url.to/api -t path/to/tests.yaml
```
