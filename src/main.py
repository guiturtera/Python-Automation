import git_integration.commands
import build_integration.commands
import click

@click.group()
def cli():
    pass

cli.add_command(git_integration.commands.git)
cli.add_command(build_integration.commands.build)