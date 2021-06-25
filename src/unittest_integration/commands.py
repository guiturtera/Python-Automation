from unittest_integration.nunit import nunit
import click

@click.group()
def unittest():
    """ Write 'flick unittest --help' for more info """
    pass

unittest.add_command(nunit)
