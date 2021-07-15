import sys
import re

import click
from click.decorators import version_option

from toradex.deploy_runner import DeployRunner
from request_facade import RequestFacade

@click.command()
@click.option('--device-name', "--dn", type=click.Path(), default="SD Card")
#@click.option('--url-path', type=click.Path(), default="pages/goldenimage.cgi")
@click.argument('resources_path', type=click.Path(exists=True))
@click.pass_context
def deploy(ctx, device_name, resources_path):
    ''' 
    flick toradex deploy [--device-name=<name>] <resources-path> 

    <resources-path>
    Full path from a folder in the computer to deploy in Toradex.
    Will copy it's content into FLASHDISK
    Note: it's not possible to copy SD Card folder!

    --device-name, --dn
    Will search into \\IP\\device-name
    The default database-adress is SD Card
    '''

    req = RequestFacade(ctx.obj['ip'], "pages/cuttree.cgi", port_number=ctx.obj['port'], login=ctx.obj['login'], password=ctx.obj['password'])
    res = DeployRunner(resources_path, req, SDCard_name=device_name).run()

    if res["Success"]: color = 'green'
    else: color = 'red'

    click.secho(res["Message"], fg=color)
    click.secho(res["ErrorMessage"], fg=color)

    sys.exit(res["ExitCode"])

