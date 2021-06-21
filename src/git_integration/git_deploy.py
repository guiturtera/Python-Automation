import re
import os
import click
from git_integration.git_manager import GitManager

@click.command()
@click.argument('repo_directory', type=click.Path(exists=True, allow_dash=True))
@click.option('--changelog', type=click.Path(exists=True, allow_dash=True), default="readme.md")
@click.option('--version-info', type=click.Path(exists=True, allow_dash=True), default="versioninfo.txt")
def deploy(repo_directory, changelog_path, versioninfo_path):
    """"
    You must specify your git directory!
    flick git deploy [git_directory_path] <options>
    
    <options>:
    --changelog=<full-path>
    Case set, will search for the changelog in the specified path
    Case not set, will search in the root [git_directory_path] for a readme.md file.

    --version-info=<full-path>
    Case set, will search for a literal str in the path, formatted as 'v1.0.0'
    Case not set, will search in the root [git_directory_path] for a versioninfo.txt path, with only the version inside it.
    """
    try:
        if changelog_path == 'changelog.md':
            changelog_path = os.path.join(repo_directory, changelog_path)
        if versioninfo_path == 'versioninfo.txt':
            versioninfo_path = os.path.join(repo_directory, versioninfo_path)

        gitManager = GitManager(repo_directory)
        lastCommits = gitManager.get_commits_since_last_release()

        for commit_type in lastCommits.keys():
            for commit in lastCommits[commit_type]:
                click.echo(click.style(commit.__str__(), fg='green'))

    except Exception as ex:
        click.echo(click.style(ex.args[0], fg='red'))
