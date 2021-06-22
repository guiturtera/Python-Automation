import os
import click

@click.command()
@click.argument('repo_directory', type=click.Path(exists=True, allow_dash=True))
@click.option('--all', type=bool, default=True, show_default=True, is_flag=True)
@click.option('--script', multiple=True)
def install_hooks(repo_directory, all, script):
    """
    You must specify your git directory!
    flick git deploy [git_directory_path] <--all> <--script="some_script">
    
    You can choose the option --all, in order to install all packages
    If all is set, --script will be ignored
    You can set multiple --script options.

    Available scripts:
    commit-msg -> validates messages that will be available to the commit-message

    """
    if all or len(script) == 0:
        click.secho('copying all', fg='green')
    elif len(script) > 1:
        click.secho(f'copying {len(script)} scripts', fg='green')
    else:
        click.secho('something went wrong... write --help for more info', fg='red')