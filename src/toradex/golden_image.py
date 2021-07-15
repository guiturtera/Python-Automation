import sys
import re

import click
from click.decorators import version_option

from toradex.golden_image_runner import GoldenImageRunner
from request_facade import RequestFacade

@click.command()
@click.option('--device-name', "--dn", type=click.Path(), default="SD Card")
#@click.option('--url-path', type=click.Path(), default="pages/goldenimage.cgi")
@click.argument('database-adress', type=click.Path(exists=True))
@click.argument('version', type=str)
@click.pass_context
def golden_image(ctx, device_name, database_adress, version):
    ''' 
    flick toradex deploy [--device-name=<name>] <database-adress> <version> 

    <database-adress>
    Full path from a folder to copy the golden image  

    <version>
    Version of the program

    --device-name, --dn
    Will search golden image into \\IP\\device-name
    The default database-adress is SD Card
    '''
    if not re.match('([0-9]+\.){2}[0-9]+$', version):
        raise click.exceptions.BadParameter('Invalid version. Must be X.Y.Z')

    req = RequestFacade(ctx.obj['ip'], "pages/goldenimage.cgi", port_number=ctx.obj['port'], login=ctx.obj['login'], password=ctx.obj['password'])
    res = GoldenImageRunner(database_adress, req, version, device_name).run()

    if res["Success"]: color = 'green'
    else: color = 'red'

    click.secho(res["Message"], fg=color)
    click.secho(res["ErrorMessage"], fg=color)

    sys.exit(res["ExitCode"])

