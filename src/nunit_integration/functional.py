import click
import sys
import re

from nunit_integration.functional_runner import FunctionalRunner
from request_facade import RequestFacade

@click.command()
@click.option('--port', type=int, default=5000)
@click.option('--auth', type=str, default="|")
@click.argument('test-to-run', type=click.Path())
@click.argument('ip', type=str)
@click.argument('url-path', type=click.Path())
def functional(port, auth, test_to_run, ip, url_path):
    ''' 
    flick nunit functional [--port=<port>] [--auth=<user>|<password>] <test_to_run> <ip> 

    Wipe all tests with more the category "UnitTest"

    <test-to-run>
    The .exe device's test absolute path to run.
    If willing to create and api, the query should have a key such as ...test_path=<test-to-run>...

    <ip>
    The ip adress of the device

    <url-path>
    The default url path

    --port
    Default is 5000
    The port number of the device to connect
    
    --auth
    If your api has Auth, you can specify it.
    '''

    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
        raise click.exceptions.BadParameter('Invalid IPV4!')
    if not re.match('^.*\|.*', auth):
        raise click.exceptions.BadParameter('Invalid auth. Write --auth-\"<user>|<password>\"')

    login, key = auth.split('|')

    req = RequestFacade(ip, url_path, port_number=port, login=login, password=key)
    success, message = FunctionalRunner(test_to_run, req).run()

    if success: color = 'green'
    else: color = 'red'

    click.secho(message, fg=color)
    #params = ["--where \"cat == UnitTest\""]
        
    #success, message = UnitRunner(test_to_run).run(params)
    #if success: color = 'green'
    #else: color = 'red'

    #click.secho(message, fg=color)