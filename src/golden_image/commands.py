import click

from golden_image.golden_image import golden_image

@click.group()
def toradex():
    """ Write 'flick unittest --help' for more info """
    pass

toradex.add_command(golden_image)