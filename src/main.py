import click

from git_integration.commands import git
from build_integration.commands import build
from nunit_integration.commands import nunit
from toradex.commands import toradex

@click.group()
def cli():
    pass

cli.add_command(git)
cli.add_command(build)
cli.add_command(nunit)
cli.add_command(toradex)

if __name__ == "__main__":
    cli()