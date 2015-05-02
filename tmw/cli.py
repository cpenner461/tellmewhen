import click
from server import app

@click.group()
def cli():
    """The basic commands in this thing."""
    pass

@cli.command()
def hello():
    """A basic hello world."""
    click.echo('Hello World Again!')

@cli.command()
def bye():
    """The opposite of hello world."""
    click.echo('Goodbye cruel world.......')

@cli.command()
def serve():
    """Run the flask server."""
    app.run()

@cli.command()
def debug():
    app.debug = True
    app.run()
