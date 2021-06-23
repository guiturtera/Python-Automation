from git_integration import git_deploy
import click

def command():
    return build

@click.group()
def build():
    """ Write 'flick build --help' for more info """
    pass

@click.command()
def msbuild():
    pass
    #git_deploy.main()

build.add_command(msbuild)
