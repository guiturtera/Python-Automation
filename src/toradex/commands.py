import click
import re

from toradex.golden_image import golden_image
from toradex.deploy import deploy

@click.group()
@click.option('--port', type=int, default=5000)
@click.option('--auth', type=str, default="|")
@click.argument('ip', type=str)
@click.pass_context
def toradex(ctx, port, auth, ip):
    """
    Write 'flick unittest --help' for more info
     
    flick toradex [--port=<port>] [--auth=<user>|<password>] <ip> <COMMAND>

    --auth
    If your api has Auth, you can specify it.

    --port
    Default is 5000
    The port number of the device to connect

    <ip>
    The ip adress of the device

    <COMMAND>
    You must specify the command to run!
    """
    ctx.ensure_object(dict)

    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
        raise click.exceptions.BadParameter('Invalid IPV4!')
    if not re.match('^.*\|.*', auth):
        raise click.exceptions.BadParameter('Invalid auth. Write --auth-\"<user>|<password>\"')

    ctx.obj['ip'] = ip
    ctx.obj['port'] = port
    ctx.obj['login'] = port
    ctx.obj['login'], ctx.obj['password'] = auth.split('|')



toradex.add_command(golden_image)
toradex.add_command(deploy)