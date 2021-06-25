from git_integration import git_deploy, git_hook
import click

@click.group()
def git():
    """ Write 'flick git --help' for more info """
    pass

git.add_command(git_deploy.deploy)
git.add_command(git_hook.install_hooks)
git.add_command(git_hook.uninstall_hooks)
