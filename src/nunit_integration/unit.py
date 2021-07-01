from nunit_integration.unit_runner import UnitRunner
import click
import os


@click.command()
@click.argument('test-to-run', type=click.Path(exists=True, allow_dash=True))
def unit(test_to_run):
    ''' 
    flick nunit unit <test_to_run>

    Wipe all tests with more the category "UnitTest"

    test-to-run
    The .exe test path to run.
    '''
    params = ["--where \"cat == UnitTest\""]
        
    success, message = UnitRunner(test_to_run).run(params)
    if success: color = 'green'
    else: color = 'red'

    click.secho(message, fg=color)