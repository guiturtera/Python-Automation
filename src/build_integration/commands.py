from git import exc
from git.cmd import Git
from git_integration import git_manager
from git_integration.git_manager import GitManager
from git_integration.version_handler import VersionHandler
from build_integration.msbuild import Msbuild
from git_integration import git_deploy

import click
import os

def command():
    return build

@click.group()
def build():
    """ Write 'flick build --help' for more info """
    pass

@click.command()
@click.option('--recursive', '-r', is_flag=True, default=False)
@click.argument('repo_directory', type=click.Path(exists=True, allow_dash=True))
@click.argument('pattern', type=str)
@click.option('--msbuild', type=click.Path(exists=True, allow_dash=True), default="C:/Windows/Microsoft.NET/Framework/v3.5/MSBuild.exe")
@click.option('--version-info', '--vinfo', type=click.Path(exists=True, allow_dash=True))
@click.option('--company-name', '--cn', type=click.Path(exists=True, allow_dash=True))

def msbuild(recursive, repo_directory, pattern, msbuild_path, version_info, company_name):
    if version_info == None:
        version_info = os.path.join(repo_directory, "versioninfo.txt")

    version_handler = VersionHandler(version_info, GitManager(repo_directory).get_commits_since_last_release())
    msbuild_builder = Msbuild(repo_directory, msbuild_path, version_info, company_name)
    try:
        if recursive:
            print('a')
            msbuild_builder.prepare_and_build_multiple(pattern)
            click.secho(f"Success to build all folders from {repo_directory}", fg="green")
        else:
            msbuild_builder.prepare_for_build()
            msbuild_builder.build()
            click.secho(f"Success to build", fg="green")
    except Exception as ex:
        for i in ex.args:
            click.secho(i, fg='red')
    

    

build.add_command(msbuild)
