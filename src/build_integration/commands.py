from git import exc
from git.cmd import Git
from git_integration import git_manager
from git_integration.git_manager import GitManager
from git_integration.version_handler import VersionHandler
from build_integration.msbuild import Msbuild
from build_integration.recursive_build import RecursiveBuilder
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
#@click.option('--project-name', type=str, default="")
@click.option('--msbuild_path', type=click.Path(exists=True, allow_dash=True), default="C:/Windows/Microsoft.NET/Framework/v3.5/MSBuild.exe")
@click.option('--version-info', '--vinfo', type=click.Path(exists=True, allow_dash=True))
@click.option('--company-name', '--cn', type=str)
def msbuild(recursive, repo_directory, pattern, msbuild_path, version_info, company_name):
    '''
    flick build [-r] msbuild <repo_directory> <pattern> [--msbuild_path=<path>] [--version-info=<path>] [--company-name=<name>]

    -r (default = false)
    recursive call. Will directly affect on the <pattern>. For more info, go to <pattern>

    <repo_directory>
    the directory from your application

    <pattern>  
    If -r is false, will ask for the .csproj file, from the root.
    e.g: "src/project/project.csproj", will search into "<repo_directory>/src/project/project.csproj"
    If -r is true, will ask for a pattern to wipe in. 
    e.g: "src/{project_name}/src" will search all the DIRECTORIES inside "<repo_directory>/src",
    get their names, and for each one, will try to find the csproj inside it.
    For example:
        - <repo_directory>
        | .git
        | libs
        | src
            | project_1
                | src
                    | project_1.csproj
                    |properties
                        |assemblyinfo.cs
            |project_2
                | src
                    | project_1.csproj
                    | properties
                        | assemblyinfo.cs
        For building both project_1 and project_2, you must specify as <pattern> "src/{project_name}/src"
        Note that, it must have {project_name}, which will be replaced by the directory name
        And also see that the directory of {project_name} must have the same text as the project.

    --company name
    specify the company name for the assembly

    --msbuild_path
    specify the msbuild path in your system. Default is windows: C:/Windows/Microsoft.NET/Framework/v3.5/MSBuild.exe

    --version-info
    Case set, will search for a literal str in the path, formatted as 'v1.0.0'
    Case not set, will search in the root <repo_directory> for a versioninfo.txt path, with only the version inside it.
    '''

    if version_info == None:
        version_info = os.path.join(repo_directory, "versioninfo.txt")

    version_handler = VersionHandler(version_info, GitManager(repo_directory).get_commits_since_last_release())
    msbuild_builder = Msbuild(repo_directory, msbuild_path, version_handler, company_name)
    try:
        if recursive:
            recursive_builder = RecursiveBuilder(msbuild_builder)
            recursive_builder.prepare_for_build(pattern)
            click.secho(recursive_builder.build(pattern), fg="green")
            #msbuild_builder.prepare_and_build_multiple(pattern)
            #click.secho(f"Success to build all folders from {repo_directory}", fg="green")
        else:
            msbuild_builder.prepare_for_build(pattern)
            click.secho(msbuild_builder.build(pattern), fg="green")
    except Exception as ex:
        for i in ex.args:
            click.secho(i, fg='red')
    

#version_handler = VersionHandler("C:\\Users\\guilherme.turtera\\Desktop\\au\\versioninfo.txt", GitManager("C:\\Users\\guilherme.turtera\\Desktop\\au").get_commits_since_last_release())
#msbuild_builder = Msbuild("C:\\Users\\guilherme.turtera\\Desktop\\au", "C:/Windows/Microsoft.NET/Framework/v3.5/MSBuild.exe", version_handler, "Presys")
#msbuild_builder.prepare_and_build_multiple("src/{project_name}/src")
#print('hello world')

build.add_command(msbuild)
