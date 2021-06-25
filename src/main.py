import click

from git_integration.commands import git
from build_integration.commands import build
from unittest_integration.commands import unittest

@click.group()
def cli():
    pass

cli.add_command(git)
cli.add_command(build)
cli.add_command(unittest)