import click

@click.group()
@click.argument('name', type=str)
@click.argument('ip', type=str)
@click.pass_context
def gp(ctx, name):
    ctx.ensure_object(dict)
    ctx.obj['name'] = name
    

@click.command()
@click.pass_context
def command1(ctx):
    print(ctx)
    print("Hello " + ctx.obj['name'])

gp.add_command(command1)
if __name__ == "__main__":
    gp()