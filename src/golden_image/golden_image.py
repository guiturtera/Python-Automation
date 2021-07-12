import sys
import re

import click
from click.decorators import version_option

from golden_image.golden_image_runner import GoldenImageRunner
from request_facade import RequestFacade

@click.command()
@click.option('--port', type=int, default=5000)
@click.option('--auth', type=str, default="|")
@click.option('--device-name', "--dn", type=click.Path(), default="SD Card")
@click.option('--url-path', type=click.Path(), default="pages/goldenimage.cgi")
@click.argument('ip', type=str)
@click.argument('database-adress', type=click.Path(exists=True))
@click.argument('version', type=str)
def golden_image(port, auth, device_name, url_path, ip, database_adress, version):
    ''' 
    flick nunit functional [--port=<port>] [--auth=<user>|<password>] [--device-name] <ip> <database-adress> <version> 

    Wipe all tests with more the category "UnitTest"

    <ip>
    The ip adress of the device

    <database-adress>
    Full path from a folder to copy the golden image  

    <version>
    Version of the program

    --port
    Default is 5000
    The port number of the device to connect
    
    --auth
    If your api has Auth, you can specify it.

    --device-name, --dn
    Will search golden image into \\IP\\database-adress
    The default database-adress is SD Card
    '''
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
        raise click.exceptions.BadParameter('Invalid IPV4!')
    if not re.match('^.*\|.*', auth):
        raise click.exceptions.BadParameter('Invalid auth. Write --auth-\"<user>|<password>\"')
    if not re.match('([0-9]+\.){2}[0-9]+$', version):
        raise click.exceptions.BadParameter('Invalid version. Must be X.Y.Z')

    login, key = auth.split('|')
    req = RequestFacade(ip, url_path, port_number=port, login=login, password=key)
    res = GoldenImageRunner(database_adress, req, version, device_name).run()

    if res["Success"]: color = 'green'
    else: color = 'red'

    click.secho(res["Message"], fg=color)
    click.secho(res["ErrorMessage"], fg=color)

    sys.exit(res["ExitCode"])

