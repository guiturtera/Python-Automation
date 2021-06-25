from unittest_integration.nunit_unit_runner import NUnitUnitRunner
import click
import os


@click.command()
@click.option('--functional', '-f', is_flag=True, default=False, show_default=True)
@click.option('--unit', '-u', is_flag=True, default=False, show_default=True)
@click.option('--all', is_flag=True, default=True, show_default=True)
@click.argument('test-to-run', type=click.Path(exists=True, allow_dash=True))
@click.option('--custom-args', type=list, show_default=True, multiple=True)
def nunit(functional, unit, all, test_to_run, custom_args):
    ''' 
    flick unittest nunit [-f] [-u] [--all] <test_to_run> [--custom-args=<args>]

    --functional, -f
    It's used to test categories of tests like: --where "cat == FunctionalTest", which means, 
    all tests of "FunctionalTest" category.
    It will make an attempt to stablish a connection with your module, and if completed, will run
    the tests inside of it.
    Note that, for this tests, the setup must be perfectly working.

    --unit, -u 
    It's are used to test categories of tests like: --where "cat == UnitTest", which means, 
    all tests of "UnitTest" category.

    test-to-run
    The .exe test path to run.

    --custom-args
    If is set, any other option will be disabled
    Search this in your nunit-console application docs.
    https://docs.nunit.org/articles/nunit/running-tests/Console-Command-Line.html
    Here the commands are from cmd, so instead of --, use /
    '''
    params = []
    if unit:
        params.append("--where \"cat == UnitTest\"")
        
    success, message = NUnitUnitRunner(test_to_run).run(params)
    if success: color = 'green'
    else: color = 'red'

    click.secho(message, fg=color)