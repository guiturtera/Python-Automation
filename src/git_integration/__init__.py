from click.decorators import command
from git_integration import git_deploy
import click

def command():
    return git

@click.group()
def git():
    """ Write 'flick git --help' for more info """
    pass

@click.command()
def deploy():
    git_deploy.main()

git.add_command(deploy)
