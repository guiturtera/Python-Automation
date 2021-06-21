import git_integration
import build_integration
import click

@click.group()
def cli():
    pass

cli.add_command(git_integration.git)
cli.add_command(build_integration.build)