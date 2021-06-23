import re
import os
import click
from git_integration.git_manager import GitManager
from git_integration.version_handler import VersionHandler
from git_integration.changelog_handler import ChangelogHandler

@click.command()
@click.argument('repo_directory', type=click.Path(exists=True, allow_dash=True))
@click.option('--changelog', type=click.Path(exists=True, allow_dash=True))
@click.option('--version-info', '--vinfo', type=click.Path(exists=True, allow_dash=True))
def deploy(repo_directory, changelog, version_info):
    """
    You must specify your git directory!
    flick git deploy [git_directory_path] <options>
    
    <options>:
    --changelog=<full-path>
    Case set, will search for the changelog in the specified path
    Case not set, will search in the root [git_directory_path] for a changelog.md file.

    --version-info=<full-path>
    Case set, will search for a literal str in the path, formatted as 'v1.0.0'
    Case not set, will search in the root [git_directory_path] for a versioninfo.txt path, with only the version inside it.
    """
    try:
        if changelog == None:
            changelog = os.path.join(repo_directory, "changelog.md")
        if version_info == None:
            version_info = os.path.join(repo_directory, "versioninfo.txt")

        gitManager = GitManager(repo_directory)
        lastCommits = gitManager.get_commits_since_last_release()

        version_handler = VersionHandler(version_info)
        changelog_handler = ChangelogHandler(changelog, lastCommits, version_handler)

        changelog_handler.apply()

        gitManager.commit_release(version_handler)

        click.secho(changelog_handler.new_text_to_append, fg='green')

    except Exception as ex:
        for i in ex.args:
                click.secho(i, fg='red')
