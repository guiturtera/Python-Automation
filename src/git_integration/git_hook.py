import os
import click
import shutil

class GitHookHandler():
    def __init__(self, repo_directory, git_hooks_directory) -> None:

        self.repo_directory = repo_directory
        self.hook_path = git_hooks_directory

        self.hook_repo_path = os.path.join(self.repo_directory, ".git", "hooks")
        self.default_git_hook = self.__validate_repo(self.hook_repo_path)


        self.__src_help_dir = os.path.join(self.hook_path, 'Help')
        self.__dst_help_dir = os.path.join(self.hook_repo_path, 'Help')

    def install(self, scripts_to_install: list =[]):
        self.remove_hook()

        if len(scripts_to_install) == 0:
            self.__install_all()
        else:
            self.__install_specific(scripts_to_install)
            self.__install_help()
    
    def __install_all(self):
        shutil.copytree(self.hook_path, self.hook_repo_path, dirs_exist_ok=True)

    def remove_hook(self):
        dir_to_erase = self.hook_repo_path
        if not len(os.listdir(dir_to_erase)) == 0:
            shutil.rmtree(dir_to_erase)
            os.mkdir(dir_to_erase)

    def __install_help(self):
        shutil.copytree(self.__src_help_dir, self.__dst_help_dir, copy_function=shutil.copy)

    def __install_specific(self, scripts_to_install):
        src_list = [os.path.join(self.hook_path, i) for i in scripts_to_install]
        # dst_list = [os.path.join(self.hook_repo_path, i) for i in scripts_to_install]
        for i in src_list:
            if not os.path.isfile(i):
                raise FileNotFoundError(f"{i} script not found! Aborted!")
        for i in range(len(src_list)):
            shutil.copy(src_list[i], self.hook_repo_path)

    def __validate_repo(self, hook_repo_path):
        if not os.path.isdir(hook_repo_path):
            raise FileNotFoundError(f"Fatal! Not a git repository! Directory \"{hook_repo_path}\" doesn't exist!")
        
        return self.__is_default_hook(hook_repo_path)


    def __is_default_hook(self, hook_repo_path) -> bool:
        for i in os.listdir(hook_repo_path):
            if not i.__contains__('.sample'):
                return False
        return True

@click.command()
@click.argument('repo_directory', type=click.Path(exists=True, allow_dash=True))
@click.option('-f', '--force', 'overwrite', type=bool, default=False, show_default=True, is_flag=True)
@click.option('--all', type=bool, default=False, is_flag=True)
@click.option('--script', multiple=True)
def install_hooks(repo_directory, overwrite, all, script):
    """
    You must specify your git directory!
    flick git deploy [-f] [git_directory_path] <--all> <--script="some_script">
    
    -f or --force -> force hooks overwrite if there's an existing hook inside the repo

    You can choose the option --all (default), in order to install all packages
    If all is set, --script will be ignored
    You can set multiple --script options.

    Available scripts:
    commit-msg -> validates messages that will be available to the commit-message

    """
    try:
        gitHookHandler = GitHookHandler(repo_directory, os.path.join(os.path.dirname(__file__), "git_hooks"))

        if not overwrite and not gitHookHandler.default_git_hook:
            raise Exception("Use --force (-f) in order to overwrite your current hooks!")

        if all or len(script) == 0:
            click.secho(f'Copying all scripts', fg='green')
            gitHookHandler.install()
            click.secho('Script(s) successfully copied!...', fg='green')
        elif len(script) > 0:
            click.secho(f'Copying {len(script)} scripts...', fg='green')
            gitHookHandler.install(script)
            click.secho('Script(s) successfully copied!...', fg='green')
        else:
            click.secho('something went wrong... write --help for more info', fg='red')

    except Exception as ex:
        for i in ex.args:
            click.secho(i, fg='red')
        click.echo(ex.with_traceback())
@click.command()
@click.argument('repo_directory', type=click.Path(exists=True, allow_dash=True))
def uninstall_hooks(repo_directory):
    """
    You must specify your git directory!
    flick git deploy [git_directory_path]
    """
    try:
        gitHookHandler = GitHookHandler(repo_directory, os.path.join(os.path.dirname(__file__), "git_hooks"))
        click.secho('Uninstalling hooks...', fg='green')
        gitHookHandler.remove_hook()
        click.secho('Successfully uninstalled!', fg='green')

    except Exception as ex:
        for i in ex.args:
            click.secho(i, fg='red')