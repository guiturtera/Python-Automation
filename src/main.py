import click

from git_integration.commands import git
from build_integration.commands import build
from nunit_integration.commands import nunit

@click.group()
def cli():
    pass

cli.add_command(git)
cli.add_command(build)
cli.add_command(nunit)
cli.add_command(test)