from nunit_integration.unit import unit
from nunit_integration.functional import functional
import click

@click.group()
def nunit():
    """ Write 'flick unittest --help' for more info """
    pass



nunit.add_command(unit)
nunit.add_command(functional)
