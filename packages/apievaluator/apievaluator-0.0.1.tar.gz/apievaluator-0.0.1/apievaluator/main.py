import json
import re
import warnings
from importlib import import_module

import click
from prance import ResolvingParser
from yaml import FullLoader, load

from apievaluator.logic import eval_all


@click.command()
@click.option(
    '-s', '--spec',
    help='Path to the spec file',
    type=click.File('r'), required=True
)
@click.option(
    '-u', '--apiurl',
    help='Base URL of the API',
    required=True
)
@click.option(
    '-t', '--tests',
    help='Path to the tests file',
    type=click.File('r'), required=True
)
@click.option(
    '-o', '--output', 'o',
    help='If specified, write to file instead of stdout',
    type=click.File('w'), default='-'
)
def main(spec: click.File, apiurl: str, tests: click.File, o: click.File):

    try:
        openApi = ResolvingParser(spec.name)
        spec = openApi.specification
        tests = load(tests, Loader=FullLoader)
    except Exception as err:
        click.echo('Error parsing input file: %s' % err)
        return

    [exists, resposes, testsDict] = eval_all(spec['paths'], apiurl, tests)

    click.echo('Summary:', file=o)
    click.echo('\tFailed:  %3d' % testsDict["failed"], file=o)
    click.echo('\tSuccess: %3d' % testsDict["success"], file=o)
    click.echo('\tTotal:   %3d' % testsDict["test"], file=o)

    click.echo('Route present checks:', file=o)
    for result in exists:
        click.echo('\t%s' % result[1], file=o)

    click.echo('Response checks:', file=o)
    for result in resposes:
        ret = result[1]

        if isinstance(ret, str):
            click.echo('\t%s' % ret, file=o)
        else:
            click.echo('\t%s' % ret[0], file=o)
            for tail in ret[1:]:
                click.echo('\t\t%s' % tail[1], file=o)


if __name__ == "__main__":
    main()
